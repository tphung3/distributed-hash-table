#import relevant libraries
import json
import os

#This file implements a manager that ensure persistency of hash table
class HashTableManager:

    #initialize instance of hash table manager with names of checkpoint/tmp chkpt, and transaction log files
    def __init__(self, chkpt_file, tmp_chkpt_file, txn_log_file):
        self.chkpt_file = chkpt_file
        self.tmp_chkpt_file = tmp_chkpt_file
        self.txn_log_file = txn_log_file

    #rebuild and return hash table from checkpoint file
    def rebuild_chkpt(self, chkpt_file):

        #if there's no checkpoint, return an empty hash table
        try:
            with open(chkpt_file, 'r') as f:
                pass    
        except FileNotFoundError:
            return {}

        #if there is a checkpoint, restore the hash table, which is supposed to be in JSON format
        try:

            #open checkpoint file
            with open(chkpt_file, 'r') as f:
                
                #load in file assuming it's in JSON format
                chkpt_hash_table = json.load(f)
                
                #check if the loaded hash table is actually of dictionary type
                if isinstance(chkpt_hash_table, dict):
                    return chkpt_hash_table
                else:
                    raise TypeError("Object loaded from checkpoint file is not a dictionary/hash table.")

        #catch exceptions
        except json.JSONDecodeError:
            raise json.JSONDecodeError("Problem when loading hash table in JSON format.", chkpt_file, 0)
        except:
            raise Exception("Problem when rebuilding hash table from checkpoint.")
            
    #replay transaction log and return updated hash table
    def replay_txn_log(self, chkpt_hash_table, txn_log_file):
            
        #if there's no logs to replay, return hash table
        try:
            with open(txn_log_file) as f:
                pass
        except FileNotFoundError:
            return chkpt_hash_table
        
        #if logs are invalid (out of date compared to the checkpoint), return hash table
        try:
            chkpt_file = self.chkpt_file
            last_mod_chkpt_t = os.path.getmtime(chkpt_file)
            last_mod_txn_log_t = os.path.getmtime(txn_log_file)

            #if logs are invalid, rename/remove them
            if (last_mod_chkpt_t > last_mod_txn_log_t):
                os.rename(txn_log_file, txn_log_file+".old")
                os.remove(txn_log_file+".old")
            else:
                pass
        except OSError:
            pass
        except:
            raise Exception("Unknown error when checking for transaction log validity.")

        #if there are valid logs to replay, modify hash table accordingly
        try:
            with open(txn_log_file, 'r') as f:
    
                #read in all lines
                log_lines = f.readlines()
                for line in log_lines:
                        
                    #remove newline character
                    line = line[:len(line)-1]
    
                    #load in each line/request and convert it to a dictionary
                    request = json.loads(line)
                    request = json.loads(request)
                    
                    #check if the loaded request is of type dictionary
                    if not isinstance(request, dict):
                        raise TypeError("Request invalid as it is not in JSON format.")
                    
                    #replay request
                    if request["method"] == "insert":
                        key = request["key"]
                        value = request["value"]
                        chkpt_hash_table[key] = value
                    elif request["method"] == "remove":
                        key = request["key"]
                        del chkpt_hash_table[key]
                    else:
                        raise Exception("Unknown method when replaying transaction log.")

        except json.JSONDecodeError:
            raise json.JSONDecodeError("Problem when loading request in JSON format.", txn_log_file, 0)

        except Exception as e:
            raise Exception("Problem when replaying transaction log.")
        return chkpt_hash_table

    #restore hash table by rebuilding hash table from checkpoint and replaying transaction log
    def restore_hash_table(self, hash_table):
        try:
            #get checkpoint and transaction log file
            chkpt_file = self.chkpt_file
            txn_log_file = self.txn_log_file
            
            #rebuild hash table from checkpoint
            chkpt_hash_table = self.rebuild_chkpt(chkpt_file)

            #replay transaction log
            hash_table = self.replay_txn_log(chkpt_hash_table, txn_log_file)
            return hash_table

        except:
            raise Exception("Unknown problem when restoring hash table from checkpoint and transaction log.")
 
    #create new checkpoint file from hash table
    def create_chkpt(self, hash_table):

        #get name of checkpoint file and its temporary and the transaction log
        chkpt_file = self.chkpt_file
        tmp_chkpt_file = self.tmp_chkpt_file
        txn_log_file = self.txn_log_file

        hash_table_dump = json.dumps(hash_table)

        #write to the temporary file
        with open(tmp_chkpt_file, "w") as f:
            f.write(hash_table_dump)
            f.flush()
            os.fsync(f)

        #ATOMIC renaming of checkpoint from temporary to permanent
        os.rename(tmp_chkpt_file, chkpt_file)

        #ATOMIC rename transaction log file
        os.rename(txn_log_file, txn_log_file+".old")
    
        #remove old transaction log file
        os.remove(txn_log_file+".old")

    #append the request to the transaction log
    def append_txn_log(self, request):

        #get transaction log file name
        txn_log_file = self.txn_log_file
       
        #jsonize the request and dump it into the transaction log
        json_request = json.dumps(request)
        with open(txn_log_file, 'a') as f:
            f.write(json_request+'\n')
            f.flush()
            os.fsync(f)
