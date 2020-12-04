from libs import *
from signatures import *
from encryption_decryption import *
from hashing import *
from blockchain import *




if __name__ == '__main__':

    private_key1, public_key1 = generate_keys()
    private_key2, public_key2 = generate_keys()
    print("Chave pública: ", public_key1)
    print("Chave privada: ", private_key1)


    message = b"encrypted data"
    # assina a mensagem com a chave privada

    msg_hashed = hashing(message)

    print("msg hashed:  ", msg_hashed)

    assinatura = sign(msg_hashed, private_key1)

    print("msg signed:  ", msg_hashed)

    #verifica com o proprietário, logo é valido
    print("is valid message ? : ", verify(msg_hashed,assinatura,public_key1))


    #verifica com o não proprietário, logo é invalido
    print("is valid message ? : ", verify(msg_hashed,assinatura,public_key2))

    #encriptada = encrypt(message, public_key1)
    #decriptada1 = decrypt(encriptada, private_key1)

    # valido
    #verifica_desencriptacao(decriptada1, message)


    # invalido
    # chave privada é diferente da criptografada
    #decriptada2 = decrypt(encriptada, private_key2)
    #verifica_desencriptacao(decriptada2, message)




    # blockchain basic

    root = CBlock('I am root', None)
    B1 = CBlock(b'I am a child.', root)
    B2 = CBlock('I am B1s brother', root)
    B3 = CBlock(12354, B1)
    B4 = CBlock(someClass('Hi there!'), B3)
    B5 = CBlock("Top block", B4)

    for b in [B1, B2, B3, B4, B5]:    
        if b.previousBlock.computeHash() == b.previousHash:
            print ("Success! Hash is good.")
        else:
            print ("ERROR! Hash is no good.")

    B3.data=12345
    if B4.previousBlock.computeHash() == B4.previousHash:
        print ("ERROR! Couldn't detect tampering.")
    else:
        print ("Success! Tampering detected.")
        
    print(B4.data)
    B4.data.num = 99999
    print(B4.data)
    if B5.previousBlock.computeHash() == B5.previousHash:
        print ("ERROR! Couldn't detect tampering.")
    else:
        print ("Success! Tampering detected.")
    