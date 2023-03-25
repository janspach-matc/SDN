

import requests
import json

def change_hostname(new_name):
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
          "cmd": "hostname " + new_name,
          "version": 1
        },
        "id": 2
      }
    ]
    response = requests.post(url,data=json.dumps(payload), verify = False, headers=myheaders,auth=(switchuser,switchpassword)).json()

def valid_name():
    valid_bool = True
    while valid_bool == True:
        hostname = input("Enter a new hostname: ")
        if hostname.isalnum():
            valid_bool = False

        else:
            print("Enter a valid hostname that is alphanumeric with no spaces.")
    return hostname

hostname = valid_name()
change_hostname(hostname)
