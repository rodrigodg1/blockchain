
import random
import string
import pickle
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

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
        self.private_key = self.load_private_key()
        self.public_key = self.load_public_key()
        self.token = "vinc"
        self.balance = 0
        self.address = id_generator()



    def load_private_key(self):
        with open("private_key.pem", "rb") as key_file:
            private_key_from_file = serialization.load_pem_private_key(
                key_file.read(),
                password=b'rodrigo',
            )
            return private_key_from_file

    def load_public_key(self):
        with open("public_key.pem", "rb") as key_file:
            public_key_from_file = serialization.load_pem_public_key(
            key_file.read()
        )
        return public_key_from_file

   

    def get_faucet(self):
        self.balance = self.balance + 10

    def assinar_transacao(self,txn):
        return self.private_key.sign(txn,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())

    def send_txn(self,txn,carteira2,assinatura):
        self.balance = self.balance - txn.valor
        carteira2.receive_txn(self.public_key,assinatura,txn)


    def verificar_transacao(self,public_key_origin_txn,assinatura,txn):
        return public_key_origin_txn.verify(assinatura,txn,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())

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

#cria carteira 1
carteira1 = Carteira()
#20 tokens
carteira1.get_faucet()
carteira1.get_faucet()


carteira2 = Carteira()


txn1 = Transaction(origem=carteira1.address,destino=carteira2.address,valor=5)
txn2 = Transaction(origem=carteira1.address,destino=carteira2.address,valor=2)

#print(txn1.to_json())
txn1 = txn1.txn_to_bytes()
assinaturatxn1 = carteira1.assinar_transacao(txn1)
txn2 = txn2.txn_to_bytes()
assinaturatxn2 = carteira1.assinar_transacao(txn2)
# envia a transacao ....

#print(txn1)

# o destino verifica se a transacao é legitima 

carteira2.show_transaction(txn1)
carteira2.show_transaction(txn2)


txn1 = carteira1.txn_bytes_to_obj(txn1)
txn2 = carteira1.txn_bytes_to_obj(txn2)
carteira1.send_txn(txn1,carteira2,assinaturatxn1)
carteira1.send_txn(txn2,carteira2,assinaturatxn2)
#carteira2.receive_txn(carteira1.public_key,assinaturatxn1,txn1)



print(carteira1.show_wallet())
print(carteira2.show_wallet())
