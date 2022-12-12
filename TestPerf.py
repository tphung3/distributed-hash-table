#import relevant libraries
import ClusterClient as CC
import sys
import time
import random

#this file implements the performance tests

#get host and port
try:
    server_base_name = sys.argv[1]
    num_servers = sys.argv[2]
    num_replicas = sys.argv[3]
except:
    print("Problem with input.")

#initialize the client
cclient = CC.ClusterClient(server_base_name, num_servers, num_replicas)

#start connection to hash table server
cclient.create_server_connections()

#set random seed to get current time
random.seed(None)

#number of operations
num_ops = 1000

#get randomized key base
key_base = random.randrange(1000, 1000000)

#bulk insertion
start = time.time()
for i in range(key_base, key_base+num_ops):
    cclient.insert("{}".format(i), '{"distributed":"systems"}')
end = time.time()
insert_result = "Throughput of {} insertions: {} ops/sec.\n".format(num_ops, num_ops/(end-start)) + "Latency of {} insertions: {} sec/op.".format(num_ops, (end-start)/num_ops)

#bulk lookup
start = time.time()
for i in range(key_base, key_base+num_ops):
    cclient.lookup("{}".format(i))
end = time.time()
lookup_result = "Throughput of {} lookups: {} ops/sec.\n".format(num_ops, num_ops/(end-start)) + "Latency of {} lookups: {} sec/op.".format(num_ops, (end-start)/num_ops)

#bulk scan
start = time.time()
for i in range(key_base, key_base+num_ops):
    cclient.scan("{}*".format(i))
end = time.time()
scan_result = "Throughput of {} scans: {} ops/sec.\n".format(num_ops, num_ops/(end-start)) + "Latency of {} scans: {} sec/op.".format(num_ops, (end-start)/num_ops)

#bulk removal
start = time.time()
for i in range(key_base, key_base+num_ops):
    cclient.remove("{}".format(i))
end = time.time()
remove_result = "Throughput of {} removals: {} ops/sec.\n".format(num_ops, num_ops/(end-start)) + "Latency of {} removals: {} sec/op.".format(num_ops, (end-start)/num_ops)

print("Final result")
print(insert_result)
print(lookup_result)
print(scan_result)
print(remove_result)

#close connection to server
cclient.close_server_connections()
