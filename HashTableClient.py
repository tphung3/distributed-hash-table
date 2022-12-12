#import relevant libraries
import socket
import sys
import json
import re
import http.client

#This file implements the hash table client
class HashTableClient:

    #initialize client with hostname and port number
    def __init__(self, project_name):
        self.project_name = project_name
        self.max_msg_len = 4294967296   #max message length is 4GBs

    #create a socket connecting to host and port
    def create_connection(self):
        if self.find_hash_table_server(self.project_name) == None:
            raise Exception("cannot find hash table server through name server.")
        (host, port) = self.find_hash_table_server(self.project_name)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host,port))
        self.sock = sock
        return sock
    
    #close connection to server
    def close_connection(self):
        self.sock.close()        

    #find server using name server
    def find_hash_table_server(self, project_name):
        name_server_name = "catalog.cse.nd.edu"
        name_server_port = 9097
        http_conn = http.client.HTTPConnection("catalog.cse.nd.edu", 9097)
        http_conn.request('GET', 'http://catalog.cse.nd.edu/query.json')
        json_msg = json.loads(http_conn.getresponse().read().decode("utf-8"))
        for entity in json_msg:
            if entity["type"] == "hashtable" and entity["project"] == project_name:
                port = int(entity["port"])
                host = entity["name"]
                return (host, port)
        return None

    #ensure that a message is sent, message should be in bytes
    def send_msg(self, msg):
        
        #get and check message's length
        len_msg = len(msg)
        if len(msg) > self.max_msg_len:
            raise Exception("Message is too long.")
        else:
            pass
        b_len_msg = len_msg.to_bytes(8, byteorder="big")

        #prepend message with length of message 
        msg = b_len_msg+msg
        len_msg = len(msg)

        #send message
        sock = self.sock
        total_sent = 0
        while (total_sent < len_msg):
            sent = sock.send(msg[total_sent:])
            if sent == 0:
                raise ConnectionError("stream broken.")
            total_sent += sent

    #receive and return a message in bytes
    def recv_msg(self):
        sock = self.sock
        total_recv = 0
        b_len_msg = b''
        while(total_recv < 8):          #first 8 bytes represent the message length
            chunk = sock.recv(8 - total_recv)
            if chunk == b'':
                raise ConnectionError("stream broken.")
            b_len_msg += chunk
            total_recv += len(chunk)

        #get length of payload
        len_msg = int.from_bytes(b_len_msg, "big")
        
        #get actual payload
        total_recv = 0
        b_payl = b''
        while(total_recv < len_msg):
            chunk = sock.recv(len_msg-total_recv)
            if chunk == b'':
                raise ConnectionError("stream broken.")
            b_payl += chunk
            total_recv += len(chunk)
        return b_payl

    #insert value to hash table via network
    def insert(self, key, value):
   
        #form a message
        msg = '{"method":"insert","key":"%s","value":%s}'% (key, value)
        
        #encode messages to byte
        b_msg = str.encode(msg)

        #send message
        self.send_msg(b_msg)

        #receive resulting message from server
        b_msg = self.recv_msg()       
 
        #get whole message
        msg = b_msg.decode("utf-8")

        #translate message to dictionary
        msg_dict = json.loads(msg)
    
        #get status of message from server
        status = msg_dict["status"]
        
        #if request is not in JSON format
        if status == "100":
            raise Exception("Invalid request from user: value not in JSON format.")

        #if method in request is invalid
        elif status == "101":
            raise Exception("Invalid request from user: invalid method.")

        #insert success with new key
        elif status == "200":
            #print("successfully insert the pair ({}, {}) with a new key".format(key, value))
            return None

        #insert success with existing key
        elif status == "201":
            #print("successfully overwrite an existing key with the pair ({}, {})".format(key, value))
            return None

        #unsuccessful insertion because of unhashable key
        elif status == "210":
            raise KeyError("unsuccessful insertion of ({}, {}) pair because of unhashable key".format(key, value))
        
        #unknown error in insertion
        elif status == "211":
            raise Exception("unknown error in insertion, please try again...")

        #unsuccessful insertion because key is not of type str
        elif status == "212":
            raise KeyError("unsuccessful insertion of key because key is not of type str.")

        #unsuccessful insertion of value because value is not a valid json document
        elif status == "213":
            raise json.JSONDecodeError("unsuccessful insertion of value because value is not a valid json document.")

        #unsuccessful insertion of value because value is not of type str, bytes, or bytearray
        elif status == "214":
            raise json.JSONDecodeError("unsuccessful insertion of value because value is not of type str, bytes, or bytearray")

        #weird error from server
        else:
            raise Exception("unknown error from server, please try again...")
       
    #lookup value in hash table via network
    def lookup(self, key):

        #form a message
        msg = '{"method":"lookup","key":"%s"}'% (key)
        
        #encode messages to byte
        b_msg = str.encode(msg)

        #send message
        self.send_msg(b_msg)

        #receive resulting message from server
        b_msg = self.recv_msg()       
 
        #get whole message
        msg = b_msg.decode("utf-8")

        #translate message to dictionary
        msg_dict = json.loads(msg)

        #get status of message from server
        status = msg_dict["status"]
        
        #get resulting value of message from server        
        try:
            ret_val = msg_dict["value"]
        except:
            pass

        #if request is not in JSON format
        if status == "100":
            raise Exception("Invalid request from user: request not in JSON format.")

        #if method in request is invalid
        elif status == "101":
            raise Exception("Invalid request from user: invalid method.")

        #lookup success with key, return key's value
        elif status == "300":
            #print("successful key lookup and return key's value.")
            ret_val = json.dumps(ret_val)
            return ret_val 
    
        #unsuccessful key lookup because of unhashable key
        elif status == "310":
            raise KeyError("unsuccessful key lookup because of unhashable key.")

        #unsuccessful key lookup because key is not in hash table
        elif status == "311":
            raise KeyError("unsuccessful key lookup because key is not in hash table.")      

        #unknown error in key lookup
        elif status == "312":
            raise Exception("unknown error in key lookup, please try again...")

        #unsuccessful key lookup because key is not of type str
        elif status == "313":
            raise KeyError("unsuccessful key lookup because key is not of type str.")

        #weird error from server
        else:
            raise Exception("unknown error from server, please try again...")
       
    #remove key and its value from hash table over network
    def remove(self, key):

        #form a message
        msg = '{"method":"remove","key":"%s"}'% (key)

        #encode messages to byte
        b_msg = str.encode(msg)

        #send message
        self.send_msg(b_msg)

        #receive resulting message from server
        b_msg = self.recv_msg()       
 
        #get whole message
        msg = b_msg.decode("utf-8")

        #translate message to dictionary
        msg_dict = json.loads(msg)

        #get status of message from server
        status = msg_dict["status"]
        
        #get resulting value of message from server        
        try:
            ret_val = msg_dict["value"]
        except:
            pass

        #if request is not in JSON format
        if status == "100":
            raise Exception("Invalid request from user: request not in JSON format.")

        #if method in request is invalid
        elif status == "101":
            raise Exception("Invalid request from user: invalid method.")

        #remove success with key, return key's value
        elif status == "400":
            #print("successful key lookup and removal of key and its value and return key's value.")
            return json.dumps(ret_val)
    
        #unsuccessful key lookup because of unhashable key
        elif status == "410":
            raise KeyError("unsuccessful key lookup and removal because of unhashable key.")

        #unsuccessful key lookup because key is not in hash table
        elif status == "411":
            raise KeyError("unsuccessful key lookup and removal because key is not in hash table.")     

        #unknown error in key lookup and removal
        elif status == "412":
            raise Exception("unknown error in key lookup and removal, please try again...")

        #unsuccessful key lookup and removal because key is not of type str
        elif status == "413":
            raise KeyError("unsuccessful key lookup and removal because key is not of type str.")

        #weird error from server
        else:
            raise Exception("unknown error from server, please try again...")

    #scan and return all pairs of (key, value) where key matches the regex
    def scan(self, regex):
    
        #form a message
        msg = '{"method":"scan","regex":"%s"}'% (regex)
        
        #encode messages to byte
        b_msg = str.encode(msg)

        #send message
        self.send_msg(b_msg)

        #receive resulting message from server
        b_msg = self.recv_msg()       
 
        #get whole message
        msg = b_msg.decode("utf-8")

        #translate message to dictionary
        msg_dict = json.loads(msg)

        #get status of message from server
        status = msg_dict["status"]
        
        #get resulting value of message from server        
        try:
            ret_val = msg_dict["value"]
        except:
            pass

        #if request is not in JSON format
        if status == "100":
            raise Exception("Invalid request from user: request not in JSON format.")

        #if method in request is invalid
        elif status == "101":
            raise Exception("Invalid request from user: invalid method.")

        #scan success and return a list of matched (key, value) pairs
        elif status == "500":
            #print("successful regex scan, and return a (possibly empty) list of  (key, value) pairs where key matches regex.")
            return ret_val 
    
        #unsuccessful regex scan because regex is not a valid regular expression
        elif status == "510":
            raise re.error("unsuccessful regex scan because regex is not a valid regular expression.")

        #unknown error in regex scan
        elif status == "511":
            raise Exception("unknown error in regex scan.")

        #no key to scan from
        elif status == "512":
            raise Exception("no keys to scan from.")

        #weird error from server
        else:
            raise Exception("unknown error from server, please try again...")
