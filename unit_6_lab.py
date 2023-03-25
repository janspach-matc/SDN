import requests
import json

# This function sends a show version command to the cli of dist-sw01 and returns the result.
# I modified the username, password and cmd to get the desired response.

def show_ver(mgmtIP):
    """
    Modify these please
    """
    switchuser='cisco'
    switchpassword='cisco'

    url='https://' + mgmtIP + '/ins' #changed to https
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
    sh_ver_response = requests.post(url,data=json.dumps(payload), verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json() #verify = False ignores cert warning
    return sh_ver_response #Type dict


def ospf_neighbor(mgmtIP):
    """
    Modify these please
    """
    switchuser='cisco'
    switchpassword='cisco'

    url='https://' + mgmtIP + '/ins' #changed to https
    myheaders={'content-type':'application/json-rpc'}
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "show ip ospf neighbor",
          "version": 1
        },
        "id": 1
      }
    ]
    ospf_response = requests.post(url,data=json.dumps(payload), verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json() #verify = False ignores cert warning
    return ospf_response #Type dict


devices = {
    "dist-sw01" : {
        "hostname" : "dist-sw01",
        "devicetype" : "switch",
        "mgmtIP" : "10.10.20.177"
        },
    "dist-sw02" : {
        "hostname" : "dist-sw02",
        "devicetype" : "switch",
        "mgmtIP" : "10.10.20.178"
        }
    }

def device_table(devices):
    print(f"Host\t\tType\tMgmtIP")
    print("-"*30)
    for device in devices.values():
        print(device["hostname"] + "\t" + device["devicetype"] + "\t" + device["mgmtIP"])
    
device_table(devices)

#sh_ver_response = show_ver(devices["dist-sw01"]["mgmtIP"])
def print_device_mem(sh_ver_response):
    print("Hostname = " + sh_ver_response["result"]["body"]["host_name"]\
          + "\t" + "Memory = " + str(sh_ver_response["result"]["body"]["memory"])\
          + " " + sh_ver_response["result"]["body"]["mem_type"]\
          + "\t Chassis = " + sh_ver_response["result"]["body"]["chassis_id"]\
          + "\t Boot File = " + sh_ver_response["result"]["body"]["kick_file_name"])

for device in devices.values():
    #print(device)
    mgmtIP = device["mgmtIP"]
    ospf_neighbor = ospf_neighbor(mgmtIP)
    print(type(ospf_neighbor))
    print(ospf_neighbor)

#print(sh_ver_response)
