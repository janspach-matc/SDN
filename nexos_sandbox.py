##Name: nexos_sandbox.py
##Author: Josh Anspach
##Date finished: 2/27/2023
##
##Script Function: Gets the hostname and memory from the dist-sw01 Devnet Sandbox switch
##and prints out the key values in a table format

import requests
import json

# This function sends a show version command to the cli of dist-sw01 and returns the result.
# I modified the username, password and cmd to get the desired response.
def show_ver():
    """
    Modify these please
    """
    switchuser='cisco'
    switchpassword='cisco'

    url='https://10.10.20.77/ins' #changed to https
    myheaders={'content-type':'application/json-rpc'}
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "show version",
          "version": 1
        },
        "id": 1
      }
    ]
    response = requests.post(url,data=json.dumps(payload), verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json() #verify = False ignores cert warning
    return response #Type dict

# Defining the response variable
response = show_ver() #Type dict

# This funtion prints the values for the nested keys host_name, memory and mem_type in a readable format
def print_device_mem(response):
    print("Hostname = " + response["result"]["body"]["host_name"] + "\t" + "Memory = " + str(response["result"]["body"]["memory"]) + " " + response["result"]["body"]["mem_type"])
    #print(type(response["result"]["body"]["host_name"]))
    #print(type(response["result"]["body"]["memory"]))
    #print(response)

# Calling the function
print_device_mem(response)
