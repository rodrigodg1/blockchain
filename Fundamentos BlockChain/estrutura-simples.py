
import random
import string
import pickle
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Transaction:
    def __init__(self,origem,destino,valor):
        self.origem = origem
        self.destino = destino
        self.valor = valor
        self.token = "vinc"

    def to_json(self):
        return {"origem": self.origem,
                "destino": self.destino,
                "valor": self.valor,
                "token": self.token}

    def txn_to_bytes(txn):
        return pickle.dumps(txn)  

    def get_origem(self):
        return self.origem

    def get_destino(self):
        return self.destino
    
    def get_valor(self):
        return self.valor



class Carteira:
    def __init__(self) -> None:
        self.private_key = ec.generate_private_key(ec.SECP384R1())
        self.public_key = self.private_key.public_key()
        self.balance = 0
        self.token = "vinc"
        self.address = id_generator()

    def get_faucet(self):
        self.balance = self.balance + 10

    def assinar_transacao(self,txn):
        return self.private_key.sign(txn,ec.ECDSA(hashes.SHA256()))

    def send_txn(self,txn):
        self.balance = self.balance - txn.valor


    def verificar_transacao(self,public_key_origin_txn,assinatura,txn):
        return public_key_origin_txn.verify(assinatura, txn, ec.ECDSA(hashes.SHA256()))


    def receive_txn(self,public_key_origin_txn,assinatura,txn):
        txn_bytes = pickle.dumps(txn) 
        transacao_invalida = self.verificar_transacao(public_key_origin_txn,assinatura,txn_bytes)
        if(transacao_invalida == None):
            print("\n Eh uma transacao VALIDA")
            #txn eh um objeto
            txn_obj = pickle.loads(txn_bytes) 
            self.balance = self.balance + txn_obj.valor



    def txn_bytes_to_obj(self,txn_bytes):
        return pickle.loads(txn_bytes) 

    def obj_to_json(self,obj):
        return {"origem": obj.origem,
                "destino": obj.destino,
                "valor": obj.valor,
                "token": obj.token}


    def show_transaction(self,txn):
        obj = self.txn_bytes_to_obj(txn)
        print("\nDetalhes da Transacao:")
        print(self.obj_to_json(obj))

    def show_wallet(self):
         return {
                'public_key': self.public_key,
                'address': self.address,   
                'balance': self.balance,
                'token':self.token
                }   





carteira1 = Carteira()
carteira1.get_faucet()
carteira1.get_faucet()
#20 tokens

carteira2 = Carteira()



txn1 = Transaction(carteira1.address,carteira2.address,20)
#print(txn1.to_json())
txn1 = txn1.txn_to_bytes()
assinaturatxn1 = carteira1.assinar_transacao(txn1)
# envia a transacao ....

#print(txn1)

# o destino verifica se a transacao é legitima 

carteira2.show_transaction(txn1)

txn1 = carteira1.txn_bytes_to_obj(txn1)

carteira1.send_txn(txn1)
carteira2.receive_txn(carteira1.public_key,assinaturatxn1,txn1)



print(carteira1.show_wallet())
print(carteira2.show_wallet())
