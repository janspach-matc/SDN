##Name: week_5_assessment.py
##Author: Josh Anspach
##Date finished: 2/21/2023
##
##Script Function: Gets a list of interfaces from the dist-sw01 Devnet Sandbox switch
##and prints out the key values in a table format


import requests
import json

"""
Be sure to run feature nxapi first on Nexus Switch

"""

#This code connects to the dist-sw01 mgmt interface and returns a dict of nested lists and dicts that contain key/value
#pairs for a list of interfaces. I put the code that Denny provided and put it into a function
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

#This function prints a header and then interates through a nested list of interfaces and prints certain values
#with tabs to line them up
def print_int_table():
    print("Name\t\tProto\t\tLink\t\tAddress")
    print("-"*60)
    for interface in response["result"]["body"]["TABLE_intf"]["ROW_intf"]:#refers to a list
        print(f"{interface['intf-name']}\t\t{interface['proto-state']}\t\t{interface['link-state']}\t\t{interface['prefix']}")#each interface is a dict





response = sh_ip_int_br()
print_int_table()




#cmd = "show ip interface brief"
#cli_api(cmd)
