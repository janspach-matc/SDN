#This script is MOSTLY working as intended. For some reason the ip_validated
#function is printing the failure notifications twice. If you can help me
#figure out why it is doing this, I'll update the script
devices = {
    "R1" : {
        "type" : "router",
        "hostname" : "R1",
        "mgmtIP" : "10.0.0.1"
        },
    "R2" : {
        "type" : "router",
        "hostname" : "R2",
        "mgmtIP" : "10.0.0.2"
        },
    "S1" : {
        "type" : "switch",
        "hostname" : "S1",
        "mgmtIP" : "10.0.0.3"
        },
    "S2" : {
        "type" : "switch",
        "hostname" : "S2",
        "mgmtIP" : "10.0.0.4"
        }
    }
#This function will iterate through the nested dictionaries and
#print each mgmtIP prepended with ping
def pingprep():
    for nest_dict in devices.values():
        print(f"ping {nest_dict['mgmtIP']}")


#This function will prompt a user to add a device and then
#add it as a nested dict to the original dictionary
def add_device():
    new_device = input("Do you want to add a new device? y or n?: ")

    if new_device == "n":
        print("No change.")

    if new_device == "y":
        new_name = input("Enter a hostname: ")
        new_dType = input("Enter a device type: ")
        new_ip = input("Enter valid mgmt ip address: ")
        ip_validated(new_ip)
        if ip_validated(new_ip) is True:
            devices[new_name] = {
                "type" : new_dType,
                "hostname" : new_name,
                "mgmtIP" : new_ip
                }
        else:
            add_device()
            
#This function validates the new mgmt IP
def ip_validated(new_ip):
    while True:
    
        new_ip_str = str(new_ip)
        new_ip_list = new_ip_str.split(".")

        if len(new_ip_list) == 4:
            A = int(new_ip_list[0])
            B = int(new_ip_list[1])
            C = int(new_ip_list[2])
            D = int(new_ip_list[3])
            if A <= 255 and B <= 255 and C <= 255 and D<=254:
                
                return True
            else:
                print("The first 3 octets must be a number between 0 and 255. The forth should be between 0 and 254.")
                return False
        else:
            print("Address must contain 4 octets")
            return False

#Calling the funtions
add_device()
pingprep()
#print(devices)

