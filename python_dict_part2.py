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
"""

This for loop iterates throught the nested dictionaries and prints the value of the key mgmtIP. 
Josh P helped me figure out how to access just the nested dict key mgmtIP when iterating 
through the for loop  

"""
for mgmtIP in devices.values():
    print(f"ping {mgmtIP['mgmtIP']}")
    #print("ping" + " " + devices["R2"]["mgmtIP"])
    #print("ping" + " " + devices["S1"]["mgmtIP"])
    #print("ping" + " " + devices["S2"]["mgmtIP"])
