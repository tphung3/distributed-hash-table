#import relevant libraries
import json
import re

#This file implements a simple hash table
class HashTable:

    #####TABLE OF RETURN CODES TO SERVER#####
    ###EACH RETURN IS A LIST OF [RETURN CODE, RETURN VALUE]
    ###INSERT
    #200: successfully insert a pair of (key, value) with a new key
    #201: successfully overwrite an existing key with the pair (key, value)
    #210: unsuccessful insertion of (key, value) pair because of unhashable key
    #211: unknown error in insertion
    #212: unsuccessful insertion of key because key is not of type str
    #213: unsuccessful insertion of value because value is not a valid json document
    #214: unsuccessful insertion of value because value is not of type str, bytes, or bytearray
    ###LOOKUP
    #300: successful key lookup and return key's value
    #310: unsuccessful key lookup because of unhashable key    
    #311: unsuccessful key lookup because key is not in hash table
    #312: unknown error in key lookup    
    #313: unsuccessful key lookup because key is not of type str
    ###REMOVE
    #400: successful key lookup, removal of key and its value from hash table, and return its value
    #410: unsuccessful key lookup because of unhashable key    
    #411: unsuccessful key lookup because key is not in hash table
    #412: unknown error in key lookup    
    #413: unsuccessful key lookup because key is not of type str 
    ###SCAN
    #500: successful regex scan, and return a (possibly empty) list of  (key, value) pairs where key matches regex
    #510: unsuccessful regex scan because regex is not a valid regular expression
    #511: unknown error in regex scan
    #512: no key to be scanned in hash table

    #hash table lives in memory
    hash_table = {}

    #set internal attributes when a new instance of a hash table is created
    def __init__(self):
        hash_table = {}
    
    #set hash table to some provided dictionay
    def set_hash_table(self, hash_table):
        self.hash_table = hash_table

    #insert key and value into hash table
    def insert(self, key, value):
        
        #if key is not hashable, don't insert (key, value) and return 210
        #if anything goes wrong, unknown error when inserting and return 211
        try:
            hash(key)
        except TypeError:
            return [210, None]
        except:
            return [211, None]

        #if key is not of type string, don't insert (key, value) and return 212
        #if anything goes wrong, unknown error when inserting and return 211
        try:
            if isinstance(key, str) == False:
                return [212, None]
        except:
            return [211, None]

        #if value is not of type str, bytes, or bytearray, don't insert (key, value) and return 214
        #if anything goes wrong, unknown error when inserting and return 211
        try:
            if not (isinstance(value, str) or isinstance(value, bytes) or isinstance(value, bytearray)):
                return [214, None] 
        except:
            return [211, None]

        #if value is not a valid JSON document, don't insert (key, value) and return 213
        #if anything goes wrong, unknown error when inserting and return 211
        try:
            json.loads(value)
        except json.JSONDecodeError:
            return [213, None]
        except:
            return [211, None]

        #if key is not in hash table, insert (key, value) and return code 200
        #if anything goes wrong, unknown error when inserting and return 211
        try:
            if key not in self.hash_table:
                self.hash_table[key] = value
                return [200, None]
        except:
            return [211, None]

        #if key is already in hash table, overwrite the key's value and return code 201
        #if anything goes wrong, unknown error when inserting and return 211
        try:
            if key in self.hash_table:
                self.hash_table[key] = value
                return [201, None]
        except:
            return [211, None]

    #lookup the value of a key in the hash table given the key
    def lookup(self, key):
        
        #if key is not hashable, don't lookup key and return 310 
        #if anything goes wrong, unknown error when inserting and return 312
        try:
            hash(key)
        except TypeError:
            return [310, None]
        except:
            return [312, None]

        #if key is not of type str, don't insert (key, value) and return 313
        #if anything goes wrong, unknown error when inserting and return 312
        try:
            if isinstance(key, str) == False:
                return [313, None]
        except:
            return [312, None]

        #if key is not in hash table, fail to find key and return 311
        #if anything goes wrong, unknown error and return 312
        try:
            if key not in self.hash_table:
                return [311, None]
        except:
            return [312, None]

        #if key is in hash table, successful key lookup and return code 300 and key's value
        #if anything goes wrong, unknown error and return 312
        try:
            if key in self.hash_table:
                val = self.hash_table[key]
                return [300, val]
        except:
            return [312, None]
    
    #remove the key and its value from hash table
    def remove(self, key):
        
        #if key is not hashable, don't find key and return 410 
        #if anything goes wrong, unknown error when inserting and return 412
        try:
            hash(key)
        except TypeError:
            return [410, None]
        except:
            return [412, None]

        #if key is not of type str, don't insert (key, value) and return 413
        #if anything goes wrong, unknown error when inserting and return 412
        try:
            if isinstance(key, str) == False:
                return [413, None]
        except:
            return [412, None]

        #if key is not in hash table, fail to find key and return 411
        #if anything goes wrong, unknown error and return 412
        try:
            if key not in self.hash_table:
                return [411, None]
        except:
            return [412, None]

        #if key is in hash table, successful key lookup, delete key and value, and return code 400 and key's value
        #if anything goes wrong, unknown error and return 412
        try:
            if key in self.hash_table:
                val = self.hash_table[key]
                del self.hash_table[key]
                return [400, val]
        except:
            return [412, None]

    #scan the list of (key, value) pairs and return all pairs where their keys match regex
    def scan(self, regex):
    
        #if regex is not a valid regular expression, don't do anything and return 510
        #if anything goes wrong, unknown error and return 511
        try:
            re.fullmatch(regex, "dummy")
        except re.error:
            return [510, None]
        except:
            return [511, None]

        #find all keys and corresponding values that match this regex and return 500
        #if there's no key, return 512
        #if anything goes wrong, unknown error and return 511
        try:
            ret_list = []
            if len(self.hash_table) == 0:
                return [512, None]
            for key in self.hash_table:
                if re.fullmatch(regex, key):
                    ret_list.append((key, self.hash_table[key]))
            return [500, ret_list]
        except:
            return [511, None]
