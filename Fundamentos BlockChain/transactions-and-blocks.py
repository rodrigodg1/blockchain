#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 09:37:13 2021

@author: rodrigodutra
"""

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature


def generate_keys():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        # gera a chave pública
        public_key = private_key.public_key()

        return private_key, public_key



# assina a transação/mensagem com a chave privada
def sign(message, private_key):
     message = bytes(str(message), 'utf-8')
     signature = private_key.sign(
     message,
     padding.PSS(
         mgf=padding.MGF1(hashes.SHA256()),
         salt_length=padding.PSS.MAX_LENGTH
     ),
     hashes.SHA256()
     )
     return signature



# verifica a validade a partir da chave publica e assinatura
def verify(message, sig, public):
    message = bytes(str(message), 'utf-8')
    try:
        public.verify(
            sig,
            message,
            padding.PSS(
              mgf=padding.MGF1(hashes.SHA256()),
              salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
    except:
        print("Error executing public_key.verify")
        return False







#cria uma conta
#com os atributos, chave privada, publica, quantidade de tokens e uma carteira com essas informações
class Account:
    
    private_key = None
    public_key = None
    amount = 0
    wallet = []
    
    def __init__(self, amount=0):
        
        #verificação se a quantidade de tokens > 0
        if(amount >= 0):
            self.amount = self.amount + amount
            self.private_key, self.public_key = generate_keys()
            print("Acc created !")    
        else:
            print("Invalid Amount\nAcc not created !")


    def get_public_key(self):
        return self.public_key
    
    def get_private_key(self):
        return self.private_key
    
    def get_amount(self):
        return self.amount
    

    
    #combina as informações sobre a conta em uma lista
    def get_wallet(self):
       
        self.wallet.append(("Private key", self.private_key))
        self.wallet.append(("Public key", self.public_key))
        self.wallet.append(("Amount tokens", self.amount))
        
        return self.wallet
    




class Tx:
    inputs = []
    outputs = []
    sigs = []
    reqd = []
    
    #o que tem em uma transação simples
    #entradas, saidas e assinaturas
    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.sigs = []
        self.reqd = []
        
    
    def add_input(self,from_addr,amount):
        self.inputs.append((from_addr,amount))
    
    def add_output(self,to_addr,amount):
        self.outputs.append((to_addr,amount))
        
    def add_reqd(self,addr):
        self.reqd.append(addr)
    

        
    def __gather(self):
        data = []
        data.append(self.inputs)
        data.append(self.outputs)
        data.append(self.reqd)
        return data
    
  
    
    def sign(self, private):
        #todas as entradas e saídas viram mensagem
        message = self.__gather()
        #assina essa mensagem com a chave privada
        newsig = sign(message, private)
        self.sigs.append(newsig)
    
    
    
    def is_valid(self):
        total_in = 0
        total_out = 0
        message = self.__gather()
        for addr, amount in self.inputs:
            found = False
            for s in self.sigs:
                if verify(message, s, addr):
                    found = True
            if not found:
                #print ("No good sig found for " + str(message))
                return False
            if amount < 0:
                return False
            total_in = total_in + amount
        for addr in self.reqd:
            found = False
            for s in self.sigs:
                if verify(message, s, addr):
                    found = True
            if not found:
                return False
        for addr, amount in self.outputs:
            if amount < 0:
                return False
            total_out = total_out + amount

        if total_out > total_in:
            #print("Outputs exceed inputs")
            return False

        return True
  
    
        
 
    
 

#informações do cabeçalho do bloco
#isso varia de plataforma para cada plataforma
class Block:
    data = None
    previousHash = None
    previousBlock = None
    id_block = 0
    
    
    def __init__(self,data,previousBlock):
        self.data = data
        self.previousBlock = previousBlock
        
        #verifica se é o bloco genesis
        #se não for, calcula o hash do bloco anterior
        if (previousBlock != None):
            self.previousHash = previousBlock.computeHash()

            #atualiza o ID do bloco
            self.id_block = self.previousBlock.id_block + 1


    #calcula o hash do bloco utilizando o SHA 256
    def computeHash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data), 'utf8'))
        digest.update(bytes(str(self.previousHash), 'utf8'))
        return digest.finalize()


    def is_valid(self):
        if self.previousBlock == None:
            return True
        #o hash das duas referencias devem ser iguais. Isto é, o do bloco atual e a do bloco anterior
        return self.previousBlock.computeHash() == self.previousHash


    
    
#criação das contas
acc1 = Account(10)
acc2 = Account(0)


#print(acc1.get_wallet())
#print(acc2.get_wallet())


#cria uma transação da conta 1 transferindo para a conta 2
tx1 = Tx()
tx1.add_input(acc1.get_public_key(),acc1.get_amount())
tx1.add_output(acc2.get_public_key(),2)
tx1.sign(acc1.get_private_key())

tx2 = Tx()
tx2.add_input(acc1.get_public_key(),acc1.get_amount())
tx2.add_output(acc2.get_public_key(),2)
tx2.sign(acc1.get_private_key())


      
if(tx1.is_valid()):
    print("Transação Válida")
   
else:
    print("Transação Inválida")





#adiciona nos blocos, as transações
#root nao tem bloco anterior, por isso none
root = Block(tx1,None)

block1 = Block(tx2,root)

#mostra os blocos
for i in [root,block1]:
    print (i.id_block)

