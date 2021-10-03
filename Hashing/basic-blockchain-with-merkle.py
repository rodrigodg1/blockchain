import hashlib
import json
from time import time
#from https://pymerkle.readthedocs.io/en/latest/tree-object.html
from pymerkle import MerkleTree

#tree = MerkleTree(b'transaction1', b'transaction2', 'transaction3')




class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        
        self.new_block(previous_hash="0", proof=100)
     
    def merkle_root(self):
        tree = MerkleTree()
        tree = MerkleTree(hash_type='sha256', encoding='utf-8', raw_bytes=True, security=True)
        tree.update(str(self.pending_transactions))
        #tree.export('tree-without-root-hash.json')
        return str(tree.rootHash.decode())
    
    def new_block(self,proof,previous_hash=None):
        block ={
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'merkle_root': self.merkle_root(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            }
    
        self.pending_transactions = []
        self.chain.append(block)
        
        return block
    
    @property
    def last_block(self):
        return self.chain[-1]
    
    def new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender':sender,
            'recipient': recipient,
            'amount': amount,
            }
    
        self.pending_transactions.append(transaction)
        return self.last_block['index'] + 1
    
    def hash(self,block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()
        
        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()
        
        return hex_hash
    
    def is_valid(self):
    
    
        for i in range(1,len(self.chain)):
            if(self.hash(self.chain[i-1]) != self.chain[i]["previous_hash"]):
                return False
        return True 
    

    

        
def check_chain():
    if(blockchain.is_valid()):
        print("Valid Chain")
    else:
        print("Invalid Chain")

    
    

blockchain = Blockchain()
t1 = blockchain.new_transaction("Rodrigo", "Ana", 50)
t2 = blockchain.new_transaction("Ana", "Rodrigo", 10)
blockchain.new_block(12345)



#print(blockchain.chain)
check_chain()



t3 = blockchain.new_transaction("Teste", "Teste2", 1100)
blockchain.new_block(12345)



#tampering
blockchain.chain[1]["amount"] = 300
#print(blockchain.chain)
print("after tampering...")
check_chain()






out_file = open("blockchain.json", "w") 
json.dump(blockchain.chain, out_file, indent = 6) 
out_file.close() 

