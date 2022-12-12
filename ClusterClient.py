#import relevant libraries
import HashTableClient
import json
import socket
import time
import http.client
import sys
import re

#implement ClusterClient class
class ClusterClient:

    #initialize this instance of ClusterClient
    def __init__(self, server_base_name, num_servers, num_replicas):
        self.num_servers = int(num_servers)
        self.num_replicas = int(num_replicas)
        self.server_base_name = server_base_name
        self.connection_table = {} #map server id to TCP connection
        #self.client = HashTableClient.HashTableClient()
        self.server_table = {}  #map server address to server id
        self.num_servers_connected = 0
        self.max_msg_len = 4294967296

    def create_server_connections(self):
        name_server_name = "catalog.cse.nd.edu"
        name_server_port = 9097
        http_conn = http.client.HTTPConnection(name_server_name, name_server_port)
        http_conn.request('GET', 'http://catalog.cse.nd.edu/query.json')
        json_msg = json.loads(http_conn.getresponse().read().decode("utf-8"))
        for entity in json_msg:
            if "type" not in entity:
                #print("NO: ", entity)
                continue
            else:
                #print("YES: ", entity)
                pass
            if entity["type"] == "hashtable" and len(entity["project"].split(self.server_base_name)) == 2:
                #print(entity)
                port = int(entity["port"])
                host = entity["name"]
                new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                new_sock.connect((host, port))
                server_id = entity["project"].split("-")[1]
                self.server_table[(host, port)] = int(server_id)
                self.connection_table[int(server_id)] = new_sock
                self.num_servers_connected += 1

    def close_server_connections(self):
        for sock in self.connection_table.values():
            sock.close()

    def send_msg(self, sock, msg):
        if isinstance(msg,int):
            pass
            #print(msg)
        len_msg = len(msg)
        if len(msg) > self.max_msg_len:
            raise Exception("Message is too long.")
        else:
            pass
        b_len_msg = len_msg.to_bytes(8, byteorder="big")
        #print(type(b_len_msg), type(msg))
        msg = b_len_msg+msg
        len_msg = len(msg)
        total_sent = 0
        while(total_sent<len_msg):
            sent = sock.send(msg[total_sent:])
            if sent == 0:
                return -1
            total_sent += sent
        return total_sent

    def recv_msg(self, sock):
        total_recv = 0
        b_len_msg = b''
        while(total_recv<8):
            chunk=sock.recv(8-total_recv)
            if chunk == b'':
                return -1
            b_len_msg+=chunk
            total_recv+=len(chunk)
        len_msg=int.from_bytes(b_len_msg,"big")
        total_recv=0
        b_payl=b''
        while(total_recv<len_msg):
            chunk=sock.recv(len_msg-total_recv)
            if chunk == b'':
                return -1
            b_payl+=chunk
            total_recv+=len(chunk)
        return b_payl

    def insert(self, key, value):
        msg='{"method":"insert","key":"%s","value":%s}'%(key,value)
        b_msg=str.encode(msg)
        start_server_id = sum([ord(char) for char in key])%self.num_servers
        i=0
        while i <self.num_replicas:
            sock = self.connection_table[(start_server_id+i)%self.num_servers]
            msg='{"method":"insert","key":"%s","value":%s}'%(key,value)
            b_msg=str.encode(msg)
            if self.send_msg(sock, b_msg) == -1:
                time.sleep(5)
                continue
            else:
                b_msg=self.recv_msg(sock)
                msg=b_msg.decode("utf-8")
                msg_dict=json.loads(msg)
                status=msg_dict["status"]
                #print(status=="201")
                if status != "201" and status != "200":
                    print("Error when inserting!")
                i+=1

    def lookup(self, key):
        msg='{"method":"lookup","key":"%s"}'%(key)
        b_msg=str.encode(msg)
        start_server_id=sum([ord(char) for char in key])%self.num_servers
        i=0
        while i<self.num_replicas:
            sock = self.connection_table[(start_server_id+i)%self.num_servers]
            msg='{"method":"lookup","key":"%s"}'%(key)
            b_msg=str.encode(msg)
            if self.send_msg(sock,b_msg) == -1:
                if i==self.num_replicas-1:
                    time.sleep(5)
                    i=0
                else:
                    i+=1
                continue
            else:
                b_msg=self.recv_msg(sock)
                msg=b_msg.decode("utf-8")
                msg_dict=json.loads(msg)
                status=msg_dict["status"]
                if status!="300":
                    return "Error when lookup key \"{}\"!".format(key)
                else:
                    return json.dumps(msg_dict["value"])

    def remove(self, key):
        msg='{"method":"remove","key":"%s"}'%(key)
        b_msg=str.encode(msg)
        start_server_id=sum([ord(char) for char in key])%self.num_servers
        i=0
        while i <self.num_replicas:
            sock = self.connection_table[(start_server_id+i)%self.num_servers]
            msg='{"method":"remove","key":"%s"}'%(key)
            b_msg=str.encode(msg)
            if self.send_msg(sock, b_msg) == -1:
                time.sleep(5)
                continue
            else:
                b_msg=self.recv_msg(sock)
                msg=b_msg.decode("utf-8")
                msg_dict=json.loads(msg)
                status=msg_dict["status"]
                if status != "400":
                    print("Error when removing!")
                i+=1
        return json.dumps(msg_dict["value"])

    def scan(self,regex):
        msg='{"method":"scan","regex":"%s"}'%(regex)
        b_msg=str.encode(msg)
        i=0
        ret = []
        while i<self.num_servers:
            sock = self.connection_table[i]
            msg='{"method":"scan","regex":"%s"}'%(regex)
            b_msg=str.encode(msg)
            if self.send_msg(sock,b_msg) == -1:
                time.sleep(5)
                continue
            else:
                b_msg=self.recv_msg(sock)
                if b_msg == -1:
                    b_msg=str.encode(msg)
                    continue
                msg=b_msg.decode("utf-8")
                msg_dict=json.loads(msg)
                status=msg_dict["status"]
                i+=1
                if status=="500":
                    if len(str(msg_dict["value"]).split("None"))==1:
                        ret.append(msg_dict["value"])
        if len(ret)==0:
            return "No keys matched regex."
        else:
            return ret
                                
