#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 08:21:20 2021

@author: rodrigodutra
"""

#https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

#private and public keys creation
#both Applications
def create_keys():
    
    private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            ) 
    public_key = private_key.public_key()
    
    return  private_key,public_key



#message signature
#both applications (A and B)
def signature_message(message,private_key):
    signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
    )

    return signature


#both applications
def check_valid_signature(signature,public_key,message):
    try:
        public_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
        )
        return "Success"
    except:
        return "Error - Invalid Sign"
    

private_key_userA,public_key_userA = create_keys()
private_key_userB,public_key_userB = create_keys()


message = b"A message I want to sign"

#create a signature
signature = signature_message(message,private_key_userA)




#in other side, check if its a valid message.
#no error
print("Error Checking if this message is coming from A: ", check_valid_signature(signature,public_key_userA,message))




#error
print("\nError Checking if this message is coming from A: ", check_valid_signature(signature,public_key_userB,message))





#both applications
def encrypt_message(message,public_key):
    cipher_text =  public_key.encrypt(
                    message,
                    padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
    )
    )
    
    return cipher_text

#in user application (local or segure storage)
def decrypt_message(ciphertext,private_key):
    decrypted = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
    )
    return decrypted


#message encryption and signature
#in User B application...
message_B = b"Message to send encrypted"

#only user A can decrypt
cipher_text_B = encrypt_message(message_B, public_key_userA)
print(cipher_text_B)
# user B sending the message
signature_B = signature_message(cipher_text_B, private_key_userB)








#in other side (User A Secure application), User A get this message and ...
print("Error Checking if this Encrypted message was signed by USER B: ",check_valid_signature(signature_B, public_key_userB, cipher_text_B))
print("Decripting...")
print(decrypt_message(cipher_text_B, private_key_userA))





