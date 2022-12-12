#import relevant libraries
import sys
import HashTable
import socket
import json
import HashTableManager
import select
import time

#receive message from client
def recv_msg(sock):
    total_recv = 0
    b_len_msg = b''
    
    #get length message
    while total_recv < 8:       #first 8 bytes represent the message length
        chunk = sock.recv(8-total_recv)
        if chunk ==b'':
            raise ConnectionError("stream broken.")
        b_len_msg += chunk
        total_recv += len(chunk)
    len_payl = int.from_bytes(b_len_msg, "big")

    #get actual payload
    total_recv = 0
    b_payl = b''
    while total_recv < len_payl:
        chunk = sock.recv(len_payl-total_recv)
        if chunk == b'':
            raise ConnectionError("stream broken.")
        b_payl += chunk
        total_recv += len(chunk)
    return b_payl

#send message back to client
def send_msg(sock, b_msg):
    len_msg = len(b_msg)
    b_len_msg = len_msg.to_bytes(8, byteorder="big")

    #prepend message with its length and send everything
    b_msg = b_len_msg + b_msg
    total_sent = 0
    while total_sent < len(b_msg):
        sent = sock.send(b_msg[total_sent:])
        if sent == 0:
            raise ConnectionError("stream broken.")
        total_sent += sent
    
#send UDP message to name server
def notify_ns(sock_port, name_server_name, name_server_port, project_name):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.connect((name_server_name, name_server_port))
    msg = '{"type":"hashtable","owner":"tphung","port": %s, "project":"%s"}' % (sock_port, project_name)
    b_msg = str.encode(msg)
    sent = udp_sock.send(b_msg)
    udp_sock.close()

#start server here
if __name__ == "__main__":
    
    #get port number and project name 
    try:
        port = 0
        project_name = sys.argv[1]
    except IndexError:
        print("You forgot to include the project name.")
        exit(1)
    except ValueError:
        print("Invalid port number.")
        exit(1)
    except:
        print("Unknown error in server side.")
        exit(2)

    #create a listening socket
    try:
        num_conn = 20
        sock = socket.create_server((socket.gethostname(),port))
    except OSError:
        print("Port {} is unavailable. Please choose a different port number.".format(port))
        exit(1)
    except Exception as e:
        print(e)
        print("Unknown error in server side.")
        exit(2)
    
    #listen to connections and perform work
    try:
        print("Listening on port {}".format(sock.getsockname()[1]))

        #socket listens for a number of connections
        sock.listen(num_conn)

        #for persistency, we have checkpoint file and its temporary version, and a transaction log
        chkpt_file = "table.ckpt"
        tmp_chkpt_file = "table.ckpt.tmp"
        txn_log_file = "table.txn"

        #initialize the hash table and its manager
        hash_table = HashTable.HashTable()
        hash_table_manager = HashTableManager.HashTableManager(chkpt_file, tmp_chkpt_file, txn_log_file)

        #restore hash table from its checkpoint and transaction log if recently crash
        hash_table.set_hash_table(hash_table_manager.restore_hash_table(hash_table))

        #initialize counter for requests to compact
        cnt_req = 0
        max_req = 100

        #initialize variables to keep track of which sockets are good for reading or writing
        pot_read = {sock:1}
        pot_write = {}
        pot_err = {}

        #timeout for UDP message, in seconds
        timeout_UDP = 60

        #sent UDP message to name server upon startup
        notify_ns(sock.getsockname()[1], "catalog.cse.nd.edu", 9097, project_name)

        start = time.time()
        #keep accepting new connections
        try:
            while True:
           
                #send UDP message to server
                if time.time() - start > timeout_UDP:
                    notify_ns(sock.getsockname()[1], "catalog.cse.nd.edu", 9097, project_name)
                    start = time.time()
                else:
                    pass
 
                #use select to check for available sockets for reading and writing, timeout in 60 seconds
                ready_read, ready_write, in_error = select.select(pot_read, pot_write, pot_err, 60)
    
                #if there's nothing, loop around again
                if len(ready_read) == 0:
                    continue
                elif len(ready_read) > 0:
                    
                    #create a socket for this client if server socket has something to read
                    if sock in ready_read:
                        conn, client_addr = sock.accept()
                        pot_read[conn] = 1
                        continue
                    
                    #receive a client's request otherwise
                    else:
                        conn = ready_read[0]

                else:
                    raise Exception("Error when using select to choose socket to read from.")

                #while client is still up
                try:
                     
                    #compact transaction log if maximum requests are reached
                    if max_req <= cnt_req:
                        hash_table_manager.create_chkpt(hash_table.hash_table) 
                        cnt_req = 0
                    else:
                        pass    
                    
                    #get request from client
                    b_msg = recv_msg(conn)

                    #get whole message from client
                    msg = b_msg.decode("utf-8")


                    #translate to dictionary
                    try: 
                        msg_dict = json.loads(msg)
    
                    #invalid request as request isn't in JSON format and return with code 100
                    except json.JSONDecodeError:
                        ret_msg = '{"status":"100"}'
                        ret_msg = str.encode(ret_msg)
                        send_msg(conn, ret_msg)
                        conn.close()
                        continue     
    
                    #get method
                    method = msg_dict["method"]

                    #insert requests
                    if method == "insert":
            
                        #get key and value
                        key = msg_dict["key"]
                        value = json.dumps(msg_dict["value"])
 
                        #get status of insertion
                        status, ret_val = hash_table.insert(key, value)
    
                        #logging this insert request only for successful requests
                        if status == 200 or status == 201:
                            hash_table_manager.append_txn_log(msg)
                            cnt_req += 1

                    #lookup requests
                    elif method == "lookup":
    
                        #get key
                        key = msg_dict["key"]
                        status, ret_val = hash_table.lookup(key)

                    #remove requests
                    elif method == "remove":
        
                        #get key
                        key = msg_dict["key"]

                        #get status of this removal            
                        status, ret_val = hash_table.remove(key)
        
                        #logging this remove request only for successful requests
                        if status == 400:
                            hash_table_manager.append_txn_log(msg)
                            cnt_req += 1

                    #scan requests
                    elif method == "scan":
                        
                        #get key
                        regex = msg_dict["regex"]
                        status, ret_val = hash_table.scan(regex)
                        ret_val = json.dumps(ret_val)       
 
                    #otherwise, invalid method and return with code 101
                    else:
                        ret_msg = '{"status":"101","value":"None"}'
                        ret_msg = str.encode(ret_msg)
                        send_msg(conn, ret_msg)
                        conn.close()
                        continue

                    #form returning messages
                    if ret_val == None:    
                        ret_msg = str.encode('{"status": "%s"}'%(status))
                    else:
                        ret_msg = str.encode('{"status": "%s", "value":%s}'%(status, ret_val))
                    send_msg(conn, ret_msg)


                except Exception as e:
                    print("{}".format(e))
                    print("Client {} has a problem. Connection shut down.".format(conn))     
                    conn.close()
                    del pot_read[conn]                

        except Exception as ex:
            print(ex)
            print("Unknown problem when accepting new connections or dealing with current connection.")

    except Exception as e:
        print(e)
        print("Unknown error in server side.")
        exit(2)
