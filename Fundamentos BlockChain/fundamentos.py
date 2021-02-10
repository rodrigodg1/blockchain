#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 08:42:22 2021

@author: rodrigodutra
"""
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


#gera as chaves privadas e publicas
#algoritmo RSA
def generate_keys():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,  
        )
        #gera a chave pública
        public_key = private_key.public_key()
        
        return private_key,public_key
    

#assina a transação/mensagem com a chave privada
def sign_message(message,private_key):

     signature = private_key.sign(
     message,
     padding.PSS(
         mgf=padding.MGF1(hashes.SHA256()),
         salt_length=padding.PSS.MAX_LENGTH
     ),
     hashes.SHA256()
     )
     return signature
    
    
#verifica a validade a partir da chave publica e assinatura
def is_valid(message,public_key,signature):
   public_key.verify(
     signature,
     message,
     padding.PSS(
         mgf=padding.MGF1(hashes.SHA256()),
         salt_length=padding.PSS.MAX_LENGTH
     ),
     hashes.SHA256()
     )
       
   
   
#encrypta a mensagem com a chave publica
def encryption(message,public_key):
       
    ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
         mgf=padding.MGF1(algorithm=hashes.SHA256()),
         algorithm=hashes.SHA256(),
         label=None
     )
    )
    return ciphertext
   


#decrypta a mensagem com a chave privada
def decryption(ciphertext,private_key):
    plaintext = private_key.decrypt(
     ciphertext,
     padding.OAEP(
         mgf=padding.MGF1(algorithm=hashes.SHA256()),
         algorithm=hashes.SHA256(),
         label=None
     )
     )
    return plaintext
   
   
   
    
    
    
    
pr1,pu1 = generate_keys()
pr2,pu2 = generate_keys()



message = b"Ola a todos"
sig1 = sign_message(message,pr1)


#se fosse um chat, eu faria a criptografia com a chave publica da outra pessoa
# e com a chave privada dela, seria descriptografado
msg_encryp = encryption(message,pu1)
print("\n\nMensagem Encryptada")
print(msg_encryp)


msg_decryp = decryption(msg_encryp,pr1)
print("\n\nMensagem Decryptada")
print(msg_decryp)




#retorna None, isto é, nenhum problema encontrado
#print(is_valid(message,pu1,sig1))




#invalido, gera uma exceção
#print(is_valid(message,pu2,sig1))


