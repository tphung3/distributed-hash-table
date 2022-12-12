#import relevant libraries
import HashTableClient as HTC
import sys
import time

#this file implements the performance tests

#get host and port
try:
    host = sys.argv[1]
    port = sys.argv[2]
except:
    print("You forgot to input hostname and port number.")

#initialize the client
htclient = HTC.HashTableClient(host, port)

#number of operations
num_ops = 1000

#bulk insertion
start = time.time()
fastest = 1000
slowest = 0
for i in range(num_ops):
    start_ind = time.time()
    htclient.insert("{}".format(i), '{"distributed":"systems"}')
    htclient.remove("{}".format(i))
    end_ind = time.time()
    if end_ind - start_ind < fastest:
        fastest = end_ind - start_ind
    elif end_ind - start_ind > slowest:
        slowest = end_ind - start_ind 
end = time.time()
result = "Fastest operation: {} seconds. Slowest operation: {} seconds.".format(fastest, slowest)

print("Final result")
print(result)
