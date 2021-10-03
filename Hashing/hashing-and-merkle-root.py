#from https://pymerkle.readthedocs.io/en/latest/tree-object.html
from pymerkle import MerkleTree

tree = MerkleTree()
tree = MerkleTree(hash_type='sha256', encoding='utf-8', raw_bytes=True, security=True)

#tree = MerkleTree(b'transaction1', b'transaction2', 'transaction3')


class Transaction:
    def __init__(self,source,destination,value):
        self.source = source
        self.destination = destination
        self.value = value
        
    def to_str(self):
        return str(self.source+self.destination+self.value)


def insert_transaction():

    origin = input("Origin: ")
    destination = input("Destination: ")
    value = input("Value: ")
    tx = Transaction(origin,destination,value)
    tx = tx.to_str()
    tree.update(tx)
    tree.export('tree-without-root-hash.json')
    
def show_tree():
    try:
        print(tree)
        print(f"Amount of nodes: {tree.size}")
        print(f"Root Hash: {tree.rootHash}")
    except:
        print("Empty tree")
    

while(True):
    op = input("1 - Insert Transaction\n2 - Show Tree\n3 - Exit \n>")
    
    if(op=="1"):
        insert_transaction()
    elif(op=="2"):
        show_tree()
    elif(op=="3"):
        break
    else:
        print("Invalid Option")







