from libs import *

# encrypt message
def encrypt(message,public_key):

    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return ciphertext



def decrypt(encrypt_message,private_key):
    plaintext = private_key.decrypt(
        encrypt_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return plaintext



def verify_decrypt(decriptada, message):

    try:

        if(decriptada == message):
            print("Mensagem Decriptada Com Sucesso: ", decriptada)

    # tratar o erro
    except:
            print("Error executing decriptation")
