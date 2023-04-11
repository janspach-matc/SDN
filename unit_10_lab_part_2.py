##Name: unit_10_lab_part_2.py
##Author: Josh Anspach
##Date finished: 4/11/2023
##
##Script Function: #Prints out the combined list of interfaces, asks the user for
##an interface to change, asks for a new ip, and prints out the updated combined list.
##Resources used were our class labs, W3 schools, and previous scripts. Lauren Wiese
##helped me combine the lists. I was trying to extract the relevant dicts from both
##the interfaces and interfaces-state output within the combinedIntList function
##modifying the first 2 functions to return an int list with only the relevant int dicts
##made combining the lists much easier!

import requests
import json

#Returns a nested list of interface dicts which is used to create a new list
#of interface dicts with only the interface name and MAC address
def getIntRestMAC(ipAddr):
    url = "https://"+ipAddr+":443/restconf/data/interfaces-state"#Connects to a web interface on the device
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
    response_json = response.json()
    intf_list = response_json["ietf-interfaces:interfaces-state"]["interface"]
    new_intf_list = []
    for intf in intf_list:
        if intf["name"] != "Loopback0":
            new_intf_list.append({"name":intf["name"], "mac":intf["phys-address"]})
    return new_intf_list

    
#Returns a nested list of interface dicts which is used to create a new list
#of interface dicts with only the interface name and IP address
def getIntRest(ipAddr):
    url = "https://"+ipAddr+":443/restconf/data/ietf-interfaces:interfaces"#Connects to a web interface on the device
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
    response_json = response.json()
    intf_list = response_json["ietf-interfaces:interfaces"]["interface"]
    new_intf_list = []
    for intf in intf_list:
        if intf["name"] != "Loopback0":
            new_intf_list.append({"name":intf["name"], "ip":intf["ietf-ip:ipv4"]["address"][0]["ip"]})
    return new_intf_list

#Takes the two interface lists from the previous functions and combines
#Them into one list the contains the interface name, IP, and MAC. 
def combineIntList(intStateList,intList):
    combinedIntList = []
    for intf in intList:
        for intf_state in intStateList:
            if intf["name"] == intf_state["name"]:
                combine = {"name":intf["name"],"ip":intf["ip"], "mac":intf_state["mac"]}
        combinedIntList.append(combine)
    
    return combinedIntList

#Prints the combined list in a table
def printList(combinedIntList):
    print("interface\t\tip\t\tmac")
    for intf in combinedIntList:
        print(intf["name"]+"\t"+intf["ip"]+"\t"+intf["mac"])

#Asks the user for an interface to change, if it passes the
#int_validated function, returns the interface.
def ask_for_int(combinedIntList):
    valid_interface = False
    while not valid_interface:    
        interface = input("Which interface would you like to assign an address to? ")
        if int_validated(interface, combinedIntList) is True:
            valid_interface = True
        else:
            print("Invalid interface. Please enter a valid and case-sensitive interface Ex. GigabitEthernet2: ")
    return interface

#Checks to see if an interface is in the combinedIntList
def int_validated(interface, combinedIntList):
    if interface in str(combinedIntList):
        return True
    else:
        return False

#Taken from a previous script
def ask_for_ip():
    valid_IP = False
    while valid_IP == False:
        ip = input("What will the new ip address be? ")
        if ip_validated(ip) == True:
            valid_IP = True
        else:
            print("Address must contain 4 octets between 0 and 255.")
    return ip

#Taken from a previous script
def ip_validated(new_ip):
    valid_bool = True
    
    new_ip_str = str(new_ip)
    new_ip_list = new_ip_str.split(".")

    if len(new_ip_list) == 4:
        A = int(new_ip_list[0])
        B = int(new_ip_list[1])
        C = int(new_ip_list[2])
        D = int(new_ip_list[3])
        if A <= 255 and B <= 255 and C <= 255 and D<=255:
                
                valid_bool = True
        else:
                
                valid_bool = False
                
    else:
        
        valid_bool = False
            
    return valid_bool

#From the TurnipTheBeet git. swapped in variables for the mgmtIP, interface to change, and new ip.
def ChangeAddressYang(ipAddr,intf_to_change,new_ip):
    url = "https://"+ipAddr+":443/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet2"
    username = 'cisco'
    password = 'cisco'
    payload={"ietf-interfaces:interface": {
                        "name": intf_to_change,
                        "description": "Configured by RESTCONF",
                        "type": "iana-if-type:ethernetCsmacd",
                        "enabled": "true",
                                         "ietf-ip:ipv4": {
                                                                "address": [{
                                                                    "ip": new_ip,
                                                                    "netmask": "255.255.255.252"
                                                                    
                                                                            }   ]
                                                            }
                                            }
             }

    headers = {
      'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm',
      'Accept': 'application/yang-data+json',
      'Content-Type': 'application/yang-data+json'
    }

    response = requests.request("PUT", url, auth=(username,password),headers=headers, verify = False, data=json.dumps(payload))
    

#MAIN SCRIPT
#Prints out the combined list of interfaces, asks the user for an interface to change,
#asks for a new ip, and prints out the updated combined list

ipAddr = "10.10.20.175"
intList = getIntRest(ipAddr)
#print(intList)
intStateList = getIntRestMAC(ipAddr)
#print(intStateList)
combinedIntList = combineIntList(intStateList, intList)
#print(combinedIntList)
printList(combinedIntList)
intf_to_change = ask_for_int(combinedIntList)
new_ip = ask_for_ip()
ChangeAddressYang(ipAddr,intf_to_change,new_ip)
intList = getIntRest(ipAddr)
intStateList = getIntRestMAC(ipAddr)
combinedIntList = combineIntList(intStateList, intList)
printList(combinedIntList)
