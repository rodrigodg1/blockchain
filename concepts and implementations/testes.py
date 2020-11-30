from libs import *
from signatures import *
from encryption_decryption import *


def verifica_desencriptacao(decriptada, message):

    try:

        if(decriptada == message):
            print("Mensagem Decriptada Com Sucesso: ", decriptada)


    except:
            print("Error executing decriptation")



if __name__ == '__main__':

    private_key1, public_key1 = generate_keys()
    private_key2, public_key2 = generate_keys()
    print("Chave pública: ", public_key1)
    print("Chave privada: ", private_key1)


    message = b"encrypted data"
    # assina a mensagem com a chave privada
    assinatura = sign(message, private_key1)


    encriptada = encrypt(message, public_key1)
    decriptada1 = decrypt(encriptada, private_key1)

    # valido
    verifica_desencriptacao(decriptada1, message)


    # invalido
    # chave privada é diferente da criptografada
    decriptada2 = decrypt(encriptada, private_key2)
    verifica_desencriptacao(decriptada2, message)
