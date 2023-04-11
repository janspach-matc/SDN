##Name: unit_8_lab.py
##Author: Josh Anspach
##Date finished: 3/26/2023
##
##Script Function: Asks a uaer for a hostname of a switch to change. If the
##switch hostname is in a dictionary of available devices, it then asks the user
##to enter a new host address for the switch. The script then connects to the switch
##using a cookie to call the api and change the hostname

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

# An attempt at trying to validate the hostname entered by the user
def valid_name():
    valid_bool = True
    while valid_bool == True:
        hostname = input("Enter a new hostname: ")
        if hostname.isascii():#I could not figure out how to allow a hostname with hyphens and underscores
            valid_bool = False

        else:
            print("Enter a valid hostname that is alphanumeric with no spaces.")
    return hostname
#Checks to see if the device to change is in our dict of available devices
def ask_device():
    device_change = input("What is the hostname of the device to change?: ")
    if device_change in device.keys():
        return device_change
    else:
        print:("That is not an available device.")
        ask_device()


#This device dict probably shouldn't be hard-coded for any practical use
device = {"dist-sw01" : "10.10.20.177", "dist-sw02" : "10.10.20.178"}

#Main script
device_change = ask_device()
address = device[device_change]
cookie = getCookie(address)
hostname = valid_name()
url = "https://"+address+"/api/node/mo/sys.json"
#print(cookie)
#/api/node/mo/sys.xml?query-target=self
#/api/node/mo/sys/ipv4/inst/dom-default.xml?query-target=children
payload = {
"topSystem": {
    "attributes": {
        "name": hostname
        }
    }
}
        
headers = {
    'Content-Type': 'application/json',
    'Cookie': 'APIC-Cookie='+cookie
}

response = requests.request("POST",url,verify=False,headers=headers,data=json.dumps(payload))
print(response.json())#The response should be {'imdata': []}
