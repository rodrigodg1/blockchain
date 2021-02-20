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
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
import pickle


#gera a chave privada e publica
def generate_keys():
    private = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )    
    public = private.public_key()
    pu_ser = public.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )    
    return private, pu_ser

#assina a mensagem com sua chave privada
def sign(message, private):
    message = bytes(str(message), 'utf-8')
    sig = private.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return sig

#verifica a validade da mensagem, com a assinatura e chave publica
def verify(message, sig, pu_ser):
    public = serialization.load_pem_public_key(
        pu_ser,
        backend=default_backend()
    )
    
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
    
    
    
    def __repr__(self):
        reprstr = "INPUTS:\n"
        for addr, amt in self.inputs:
            reprstr = reprstr + str(amt) + " from " + str(addr) + "\n"
        reprstr = reprstr + "OUTPUTS:\n"
        for addr, amt in self.outputs:
            reprstr = reprstr + str(amt) + " to " + str(addr) + "\n"
        reprstr = reprstr + "REQD:\n"
        for r in self.reqd:
            reprstr = reprstr + str(r) + "\n"
        reprstr = reprstr + "SIGS:\n"
        for s in self.sigs:
            reprstr = reprstr + str(s) + "\n"
        reprstr = reprstr + "END\n"
        return reprstr
  
    
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


    






class TxBlock (Block):

    valid_transactions_count = 0
    

    def __init__(self, previousBlock):
        super(TxBlock, self).__init__([],previousBlock)
        

# adiciona uma transação ao bloco como dados
#contagem das transações válidas no bloco
    def count_valid_transactions(self):
        for tx in self.data:
            if tx.is_valid():
                self.valid_transactions_count = self.valid_transactions_count + 1
            
        return self.valid_transactions_count
                


    def addTx(self, Tx_in):
        self.data.append(Tx_in)


#verifica se as transações no bloco são válidas
#percorre as transações armazenadas como dados no bloco
#e verifica se essas transações são válidas
    def is_valid(self):
        if not super(TxBlock, self).is_valid():
            return False
        for tx in self.data:
            if not tx.is_valid():
                return False

        return True




class Blockchain:
    count_blocks = 0
    chain = []
    id_chain = ""

    #nome para a cadeia
    def __init__(self,id_chain):
        self.id_chain = id_chain

    def add_block(self,block):
        self.chain.append(block)
        self.count_blocks = self.count_blocks + 1





if __name__ == '__main__':

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
    
    
    
    tx3 = Tx()
    tx3.add_input(acc2.get_public_key(),acc2.get_amount())
    tx3.add_output(acc1.get_public_key(),4)
    tx3.sign(acc2.get_private_key())
    
    
    
    
    
          
    if(tx1.is_valid()):
        print("Transação Válida")
       
    else:
        print("Transação Inválida")
    
    
    
    #adiciona nos blocos, as transações
    #root nao tem bloco anterior, por isso none
    root = TxBlock(None)
    root.addTx(tx1)
    root.addTx(tx2)
    
    
    block1 = TxBlock(root)
    block1.addTx(tx2)
    
    
    #salva as transações em um arquivo
    savefile = open("block.dat", "wb")
    pickle.dump(block1, savefile)
    savefile.close()
    
 
    #carrega esse arquivo
    loadfile = open("block.dat", "rb")
    load_B1 = pickle.load(loadfile)
    
    
    #verifica se esse arquivo é valido
    if load_B1.is_valid():
        print("Sucess! Loaded Tx is valid")
    else:
        print("Fail ! Tx block is invalid")
    loadfile.close()
    
    
    
    #cria um blockchain
    blockchain = Blockchain("My-Chain")
    
    print("\n\n"+ blockchain.id_chain)

    
    # verifica os blocos criados aqui e tbm dos arquivos
    for b in [root, block1,load_B1]:
        print(f"\nblock {b.id_block}")
        if b.is_valid():
            print("Success! Valid block")
            print("Inserting into blockchain...")
            blockchain.add_block(b)
        else:
            print("ERROR! Bad block")

    # mostra a quantidade de blocos na cadeia
    print(f"\n\nCount block (height) blockchain: {blockchain.count_blocks}")

