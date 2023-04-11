devices = [
    {
        "hostname": "R1",
        "type": "router",
        "brand": "Cisco",
        "mgmtIP": "10.0.0.1"
        },
    {
        "hostname": "S1",
        "type": "switch",
        "brand": "Cisco",
        "mgmtIP": "10.0.0.2"
        }
    ]

def createListSubset(ListOfDevs): #Accepts a full list of dicts and returns a modified list of dicts that contains only a hostname and address

    NewList = []

    for dev in ListOfDevs:
         NewList.append({"hostname": dev["hostname"], "mgmtIP": dev["mgmtIP"]}) #appends a new list of dictionaries

    return NewList

print(devices)

modList = createListSubset(devices)

print(modList)

for device in modList:
    print(device)
