##Name: unit_7_lab.py
##Author: Josh Anspach
##Date finished: 3/5/2023
##
##Script Function: Makes an api call to a cisco sandbox switch and prints in a table.
##Asks the user for an interface to modify.
##Asks the user for the new ip and CIDR for the requested interface. Validates all user input
##and applies the new ip to the interface. Prints the updated inteface table.




import requests
import json

"""
Be sure to run feature nxapi first on Nexus Switch

"""
#This function returns a dict with info from the cli using sh ip int br

def sh_ip_int_br():
    switchuser='cisco'
    switchpassword='cisco'

    url='https://10.10.20.177/ins'
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

#Prints a pretty table with the sh ip int br response
def print_int_table(response):
    print("Name\t\tProto\t\tLink\t\tAddress")
    print("-"*60)
    for interface in response["result"]["body"]["TABLE_intf"]["ROW_intf"]:#refers to a list
        print(f"{interface['intf-name']}\t\t{interface['proto-state']}\t\t{interface['link-state']}\t\t{interface['prefix']}")#each interface is a dict

#Function sends the commands needed to change the ip of an interface using
#variables from the user input functions
def change_int_ip(interface, ip, cidr):
    """
    Modify these please
    """
    switchuser='cisco'
    switchpassword='cisco'

    url='https://10.10.20.177/ins'
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
          "cmd": "ip address " + ip + "/" + cidr,
          "version": 1
        },
        "id": 3
      }
    ]
    response = requests.post(url,data=json.dumps(payload), verify=False, headers=myheaders,auth=(switchuser,switchpassword)).json()
    #Nothing to return

#Validates an ip consists of 4 octets with a number ranging from 0-255.
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

#Validates an interface exists in a list of interfaces from the api response for sh ip int br.
def int_validated(interface, response):
    interfaces = [intf['intf-name'] for intf in response["result"]["body"]["TABLE_intf"]["ROW_intf"]]
    return interface in interfaces
    
#Validates a CIDR number is between 1 and 32
def cidr_validated(cidr):
    valid_bool = True
    if int(cidr) > 0 and int(cidr) < 33:
        valid_bool = True
    else:
        valid_bool = False
    return valid_bool

#Asks the user for an interface to change and returns the interface upon validation.
def ask_for_int(response):
    valid_interface = False
    while not valid_interface:    
        interface = input("Which interface would you like to assign an address to? ")
        if int_validated(interface, response):
            valid_interface = True
        else:
            print("Invalid interface. Please enter a valid interface")
    return interface

#Asks the user for an ip address and returns the address upon validation.
def ask_for_ip():
    valid_IP = False
    while valid_IP == False:
        ip = input("What will the new ip address be? ")
        if ip_validated(ip) == True:
            valid_IP = True
        else:
            print("Address must contain 4 octets between 0 and 255.")
    return ip
  
#Asks the user for a CIDR and returns it upon validation.
def ask_for_cidr():
    valid_cidr = False
    while valid_cidr == False:
        cidr = input("What will the CIDR be? ")
        if cidr_validated(cidr) == True:
            valid_cidr = True
        else:
            print("The CIDR must be a number between 1 and 32.")
    return cidr

#Defines a variable for the api response to sh ip int br    
response = sh_ip_int_br()#Dict

#print(type(response))
#print(response)

#Prints repsonse in a pretty table
print_int_table(response)

#Defines the requested interface
interface = ask_for_int(response)#Str

#Defines the requested ip
ip = ask_for_ip()#Str

#Defines the requested CIDR number
cidr = ask_for_cidr()#Str


#Calls the function that sends commands to the api for an interface ip change
change_int_ip(interface, ip, cidr)

#Defines a the response with the updated interface IP info
response = sh_ip_int_br()

#Prints out the updated interface ip table
print_int_table(response)
#print(response)
#print(response["result"]["body"]["TABLE_intf"]["ROW_intf"])
