#import relevant libraries
import ClusterClient as CC
import sys

#this file implements the basic tests

#get host and port
try:
    server_base_name = sys.argv[1]
    num_servers = sys.argv[2]
    num_replicas = sys.argv[3]
except:
    print("Problems with input.")

#initialize the client
#set max message length
max_msg_len = 4294967296        #4GBs
cclient = CC.ClusterClient(server_base_name, num_servers, num_replicas)

#start connection to hash table server
cclient.create_server_connections()

#CHANGE THIS VARIABLE for various cases, pick any integer from 0 to 6
case = 0

if case == 0:

    #insert new key and value
    cclient.insert("zebra", '{"cool": "cool"}')

    #insert new key and value
    cclient.insert("zebro", '{"cool": {"cool":"cool"}}')
    
    #lookup key
    print(cclient.lookup("zebra"))

    #lookup key
    print(cclient.lookup("zebra"))

    #lookup key
    print(cclient.lookup("zebro"))

    #scan for zebra
    print(cclient.scan("zeb.*"))

    #remove key
    print(cclient.remove("zebro"))

    #remove key
    print(cclient.remove("zebra"))

    #remove key again -> exception
    #print(cclient.remove("zebra"))

elif case == 1:

    #lookup key, assuming hash table is empty -> exception
    print(cclient.lookup("zebra"))

elif case == 2:

    #remove key, assuming hash table is empty -> exception
    print(cclient.remove("zebra"))

elif case == 3:

    #scan regex, assuming hash table is empty -> exception
    print(cclient.scan("zeb.*"))

elif case == 4:

    #insert invalid JSON value -> exception
    cclient.insert("zebra", '{cool": "cool"}')

elif case == 5:

    #scan with invalid regex -> exception
    print(cclient.scan("*."))

elif case == 6:
    #insert new key and value
    cclient.insert("zebra", '{"cool": "cool"}')

    #insert new key and value
    cclient.insert("zebro", '{"cool": {"cool":"cool"}}')
    
    #lookup key
    print(cclient.lookup("zebra"))

    #lookup key
    print(cclient.lookup("zebra"))

    #lookup key
    print(cclient.lookup("zebro"))

    #scan for zebra
    print(cclient.scan("zeb.*"))

    #remove key
    print(cclient.remove("zebro"))

    #remove key
    print(cclient.remove("zebra"))

    #lookup removed key -> exception
    print(cclient.lookup("zebra"))

#close connection to server
cclient.close_server_connections()
