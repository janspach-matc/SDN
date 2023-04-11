##Name: unit_9_lab.py
##Author: Josh Anspach
##Date finished: 4/9/2023
##
##Script Function: Uses a REST API call to get a dict of interfaces then prints
##out the name, ip address, and subnet mask of each interface

import requests
import json

def get_interfaces(mgmt_IP):
    #url = "https://10.10.20.175:443/restconf/data/ietf-yang-library:modules-state"
    #url = "https://10.10.20.175:443/restconf/tailf/modules/ietf-interfaces/2014-05-08"
    url = "https://"+mgmt_IP+":443/restconf/data/ietf-interfaces:interfaces"#Connectes to a web interface on the device
    username = 'cisco'
    password = 'cisco'
    payload={}
    headers = {
      'Content-Type': 'application/yang-data+json',
      'Accept': 'application/yang-data+json',
      'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm'
    }

    response = requests.request("GET", url, auth = (username,password), verify = False, headers=headers, data=payload)
    #print(response.text)
    #print(str(response["ietf-interfaces:interfaces"]["interface"][0]["ietf-ip:ipv4"]["address"][0]))
    return response.json()

def print_interfaces(intDict):
    #print(intDict)
    intList =  intDict['ietf-interfaces:interfaces']['interface']
    #print(intList)
    for intf in intList:
        for ip_addr in intf['ietf-ip:ipv4']['address']:
            print(intf['name']+"\t"+ip_addr['ip']+"\t"+ip_addr['netmask'])


mgmt_IP = "10.10.20.175"
intDict = get_interfaces(mgmt_IP)
#print(intDict)
print_interfaces(intDict)


##"name": "ietf-interfaces",
##        "revision": "2014-05-08",
##        "schema": "https://10.10.20.175:443/restconf/tailf/modules/ietf-interfaces/2014-05-08"
