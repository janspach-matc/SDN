servers = {
    "Server1" : "221.100.250.75",
    "Server2" : "201.0.113.22",
    "Server3" : "58.23.191.6"
    }

#This variable is a list of the servers dictionary values
#used for the PingPrep function
ipList = servers.values()

#This function prints the Server IP table
def server_table(servers):
    print("Server Name" + '\t' + "Address")
    print("-" * 90)
    for item in servers.items():
        print(f"{item[0]} \t {item[1]}")

#This function iterates though the ipList
#and prepends each with "Ping"        
def PingPrep(ipList):
    for value in ipList:
        print("Ping " + value)

#Here is where I call both functions
server_table(servers)
PingPrep(ipList)
#print(ipList)
