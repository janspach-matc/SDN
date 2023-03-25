##Name: midterm.py
##Author: Josh Anspach
##Date finished: 3/18/2023
##
##Script Function:Iterates through a dict of cisco sandbox switch's mgmtIP addresses and updates the ip address
##of each VLAN interface on the switch. Prints a before and after interface table showing only Vlan interfaces.






import requests
import json

"""
Be sure to run feature nxapi first on Nexus Switch

"""
#This function takes a mgmtIP var and returns a dict with info from the cli using sh ip int br

def sh_ip_int_br(mgmt_ip):
    switchuser='cisco'
    switchpassword='cisco'

    url='https://'+mgmt_ip+'/ins'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "show ip interface brief",
          "version": 1
        },
        "id": 1
      }
    ]
    response = requests.post(url,data=json.dumps(payload), verify=False,headers=myheaders,auth=(switchuser,switchpassword)).json()
    return response

#Prints a pretty table for ONLY Vlan interfaces with the sh ip int br response
def print_int_table(response):
    print("Name\t\tProto\t\tLink\t\tAddress")
    print("-"*60)
    for interface in response["result"]["body"]["TABLE_intf"]["ROW_intf"]:#refers to a list
        if interface['intf-name'].startswith("V"):#startswith method learned from Josh P/w3 schools
            print(f"{interface['intf-name']}\t\t{interface['proto-state']}\t\t{interface['link-state']}\t\t{interface['prefix']}")#each interface is a dict

#Function sends the commands needed to change the ip of an interface using
#variables interface, new_ip and mgmt_ip
def change_int_ip(interface, new_ip, mgmt_ip):
    """
    Modify these please
    """
    switchuser='cisco'
    switchpassword='cisco'

    url='https://'+mgmt_ip+'/ins'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "configure terminal",
          "version": 1
        },
        "id": 1
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "interface " + interface,
          "version": 1
        },
        "id": 2
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "ip address " + new_ip + "/24",
          "version": 1
        },
        "id": 3
      }
    ]
    response = requests.post(url,data=json.dumps(payload), verify=False, headers=myheaders,auth=(switchuser,switchpassword)).json()
    #Nothing to return
#This function breaks an ip address into a list and adds 5 to the 4th octet
def ip_add_5(ip_changed):
    octet_list = ip_changed.split(".")
    octet_changed = octet_list[3]
    octet_updated = int(octet_changed) + 5
    octet_list[3] = str(octet_updated)
    new_ip = ".".join(octet_list)#join method learned from Josh P/w3 schools
    #print(new_ip)
    return new_ip

#Making a dictionary so we have a way to iterate through multiple devices
device = {"dist-sw01" : "10.10.20.177", "dist-sw02" : "10.10.20.178"}
#print(device.items())

#Main script that iterates though the device dict and updates the Vlan interface's
#ip addresses
for item in device.items():
    #device_name = item[0]
    mgmt_ip = item[1]
    #print(device_name)
    #print(mgmt_ip)
    response = sh_ip_int_br(mgmt_ip)
    print_int_table(response)
    for interface in response["result"]["body"]["TABLE_intf"]["ROW_intf"]:#refers to a list
        if interface['intf-name'].startswith("V"):
            ip_changed = interface['prefix']
            new_ip = ip_add_5(ip_changed)
            interface = interface['intf-name']
            change_int_ip(interface, new_ip, mgmt_ip)
    #print(response)
    #int_list = response["result"]["body"]["TABLE_intf"]["ROW_intf"]
    #print(int_list)
    response = sh_ip_int_br(mgmt_ip)
    print_int_table(response)
#ip_changed = "172.16.101.2"    
#ip_add_5(ip_changed)
