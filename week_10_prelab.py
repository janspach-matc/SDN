##Name: week_10_prelab.py
##Author: Josh Anspach
##Date finished: 4/3/2023
##
##Script Function: Gets a list of dictionaries with interface data and prints out only
##the domain and interface id for each ipv4 interface in the list

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

#Gets a list of dictionaries with each ipv4 interface in the default domain 
def get_ipv4_interfaces(addr,cookie):
    url = "https://"+addr+"/api/node/mo/sys/ipv4/inst/dom-default.json?query-target=children"
    payload = {}
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'APIC-Cookie='+cookie
    }
    response = requests.request("GET",url,verify=False,headers=headers,data=json.dumps(payload))
    return response.json()

#Prints the domain and interface id of each interface in the list imdata
def print_ipv4_int(ipv4_interfaces):
    for interface in ipv4_interfaces["imdata"]:
        print (interface["ipv4If"]["attributes"]["dn"] + "  " + interface["ipv4If"]["attributes"]["id"])

addr = "10.10.20.177"
cookie = getCookie(addr)
#print(cookie)
ipv4_interfaces = get_ipv4_interfaces(addr,cookie)
#print (ipv4_interfaces)
print_ipv4_int(ipv4_interfaces)
#/api/node/mo/sys.xml?query-target=self
#/api/node/mo/sys/ipv4/inst/dom-default.xml?query-target=children
