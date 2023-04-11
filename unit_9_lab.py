##Name: unit_9_lab.py
##Author: Josh Anspach
##Date finished: 4/9/2023
##
##Script Function: Iterates through a dictionary of devices and creates a named vlan,
##makes it an SVI with an ip, configures HSRP for the SVI, and assigns an OSPF area/process ID

import requests
import json

def getCookie(addr) :

#NX REST API Authen See REST API Reference for format of payload below

    url = "https://"+ addr + "/api/aaaLogin.json"
 
    payload= {"aaaUser" :
              {"attributes" :
                   {"name" : "cisco",
                    "pwd" : "cisco"}
               }
          }

    response = requests.post(url,json=payload,verify=False)
    #print(response.json())
    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]

#Uses NAXPI DME model to take a mgmtIP, cookie and VLAN info. Creates and names a VLAN
def create_vlan(addr,vlan_numb,vlan_name,cookie):
    url = "https://"+addr+"/api/node/mo/sys.json"
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'APIC-Cookie='+cookie
    }
    payload ={
      "topSystem": {
        "children": [
          {
            "bdEntity": {
              "children": [
                {
                  "l2BD": {
                    "attributes": {
                      "fabEncap": vlan_numb,
                      "name": vlan_name
                    }
                  }
                }
              ]
            }
          }
        ]
      }
    }
    response = requests.request("POST",url,verify=False,headers=headers,data=json.dumps(payload))
    return response.json()

#Uses NAXPI DME model to take a mgmtIP, cookie and interface info. Creates and assigns an ip to an int.
def create_svi(addr,int_name,new_ip,cookie):
    url = "https://"+addr+"/api/node/mo/sys.json"
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'APIC-Cookie='+cookie
    }
    payload ={
      "topSystem": {
        "children": [
          {
            "ipv4Entity": {
              "children": [
                {
                  "ipv4Inst": {
                    "children": [
                      {
                        "ipv4Dom": {
                          "attributes": {
                            "name": "default"
                          },
                          "children": [
                            {
                              "ipv4If": {
                                "attributes": {
                                  "id": int_name
                                },
                                "children": [
                                  {
                                    "ipv4Addr": {
                                      "attributes": {
                                        "addr": new_ip
                                      }
                                    }
                                  }
                                ]
                              }
                            }
                          ]
                        }
                      }
                    ]
                  }
                }
              ]
            }
          },
          {
            "interfaceEntity": {
              "children": [
                {
                  "sviIf": {
                    "attributes": {
                      "adminSt": "up",
                      "id": int_name
                    }
                  }
                }
              ]
            }
          }
        ]
      }
    }
    response = requests.request("POST",url,verify=False,headers=headers,data=json.dumps(payload))
    return response.json()

#Uses NAXPI DME model to take a mgmtIP, cookie and HSRP info. Configures HSRP on an interface.

def hsrp_config(addr,int_name,hsrp_group,hsrp_addr,cookie):
    url = "https://"+addr+"/api/node/mo/sys.json"
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'APIC-Cookie='+cookie
    }
    payload ={
      "topSystem": {
        "children": [
          {
            "interfaceEntity": {
              "children": [
                {
                  "sviIf": {
                    "attributes": {
                      "id": int_name
                    }
                  }
                }
              ]
            }
          },
          {
            "hsrpEntity": {
              "children": [
                {
                  "hsrpInst": {
                    "children": [
                      {
                        "hsrpIf": {
                          "attributes": {
                            "id": int_name
                          },
                          "children": [
                            {
                              "hsrpGroup": {
                                "attributes": {
                                  "af": "ipv4",
                                  "id": hsrp_group,
                                  "ip": hsrp_addr,
                                  "ipObtainMode": "admin"
                                }
                              }
                            }
                          ]
                        }
                      }
                    ]
                  }
                }
              ]
            }
          }
        ]
      }
    }
    response = requests.request("POST",url,verify=False,headers=headers,data=json.dumps(payload))
    return response.json()

#Uses NAXPI DME model to take a mgmtIP, cookie and OSPF info. Configures OSPF on an interface.
def ospf_config(addr,int_name,ospf_id,ospf_area,cookie):
    url = "https://"+addr+"/api/node/mo/sys.json"
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'APIC-Cookie='+cookie
    }
    payload ={
      "topSystem": {
        "children": [
          {
            "ospfEntity": {
              "children": [
                {
                  "ospfInst": {
                    "attributes": {
                      "name": ospf_id
                    },
                    "children": [
                      {
                        "ospfDom": {
                          "attributes": {
                            "name": "default"
                          },
                          "children": [
                            {
                              "ospfIf": {
                                "attributes": {
                                  "advertiseSecondaries": "yes",
                                  "area": ospf_area,
                                  "id": int_name
                                }
                              }
                            }
                          ]
                        }
                      }
                    ]
                  }
                }
              ]
            }
          },
          {
            "interfaceEntity": {
              "children": [
                {
                  "sviIf": {
                    "attributes": {
                      "id": "vlan110"
                    }
                  }
                }
              ]
            }
          }
        ]
      }
    }
    response = requests.request("POST",url,verify=False,headers=headers,data=json.dumps(payload))
    return response.json()

#This device dict probably shouldn't be hard-coded for any practical use
#device = {"dist-sw01" : "10.10.20.177", "dist-sw02" : "10.10.20.178"}

#Main script

devices = {"dist-sw01" : "10.10.20.177", "dist-sw02" : "10.10.20.178"}

#Iterates through device dict and configures a Vlan SVI with OSPF and HSRP
#for each device
for device in devices.values():
    mgmt_IP = device
    #print(mgmt_IP)
    cookie = getCookie(mgmt_IP)
    vlan_numb = "vlan-110"
    vlan_name = "testNXOS"
    int_name = "vlan110"
    #Probably a better way of automating this
    if mgmt_IP == "10.10.20.177":
        new_ip = "172.16.110.2/24"
    if mgmt_IP == "10.10.20.178":
        new_ip = "172.16.110.3/24"
    hsrp_group = "10"
    hsrp_addr = "172.16.110.1"
    ospf_id = "1"
    ospf_area = "0.0.0.0"
    create_vlan(mgmt_IP,vlan_numb,vlan_name,cookie)
    create_svi(mgmt_IP,int_name,new_ip,cookie)
    hsrp_config(mgmt_IP,int_name,hsrp_group,hsrp_addr,cookie)
    ospf_config(mgmt_IP,int_name,ospf_id,ospf_area,cookie)
    
##mgmt_IP = "10.10.20.177"
##cookie = getCookie(mgmt_IP)
##vlan_numb = "vlan-110"
##vlan_name = "testNXOS"
##int_name = "vlan110"
##new_ip = "172.16.110.2/24"
##hsrp_group = "10"
##hsrp_addr = "172.16.110.1"
##ospf_id = "1"
##ospf_area = "0.0.0.0"
##create_vlan(mgmt_IP,vlan_numb,vlan_name,cookie)
##create_svi(mgmt_IP,int_name,new_ip,cookie)
##hsrp_config(mgmt_IP,int_name,hsrp_group,hsrp_addr,cookie)
##ospf_config(mgmt_IP,int_name,ospf_id,ospf_area,cookie)
##
##mgmt_IP = "10.10.20.178"
##cookie = getCookie(mgmt_IP)
##vlan_numb = "vlan-110"
##vlan_name = "testNXOS"
##int_name = "vlan110"
##new_ip = "172.16.110.3/24"
##hsrp_group = "10"
##hsrp_addr = "172.16.110.1"
##ospf_id = "1"
##ospf_area = "0.0.0.0"
##create_vlan(mgmt_IP,vlan_numb,vlan_name,cookie)
##create_svi(mgmt_IP,int_name,new_ip,cookie)
##hsrp_config(mgmt_IP,int_name,hsrp_group,hsrp_addr,cookie)
##ospf_config(mgmt_IP,int_name,ospf_id,ospf_area,cookie)
