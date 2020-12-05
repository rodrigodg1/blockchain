from libs import *
from signatures import *
from encryption_decryption import *
from hashing import *
from blockchain import *


if __name__ == '__main__':

    '''
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

    # verifica com o proprietário, logo é valido
    print("is valid message ? : ", verify(msg_hashed, assinatura, public_key1))

    # verifica com o não proprietário, logo é invalido
    print("is valid message ? : ", verify(msg_hashed, assinatura, public_key2))

    encriptada = encrypt(message, public_key1)
    decriptada1 = decrypt(encriptada, private_key1)

    # valido
    verify_decrypt(decriptada1, message)

    # invalido
    # chave privada é diferente da criptografada
    decriptada2 = decrypt(encriptada, private_key2)
    verify_decrypt(decriptada2, message)

    '''
# criação dos blocos
    root = CBlock('I am root', None)
    B1 = CBlock(b'I am a child.', root)
    B2 = CBlock('I am B1s brother', root)
    B3 = CBlock(12354, B1)
    B4 = CBlock(someClass('Hi there!'), B3)
    B5 = CBlock("a+b+c", B4)
    B6 = CBlock("c+3+c2+2", B5)

   # percorre op blockchain verificando se é válido, isto é
   # se o hash do bloco anterior é igual ao previous hash do bloco atual
    for b in [B1, B2, B3, B4, B5, B6] :
        if b.previousBlock.computeHash() == b.previousHash:
            print("Success! Hash is good.")
        else:
            print("ERROR! Hash is no good.")

    # alteração de registros
    B3.data = 12345
    if B4.previousBlock.computeHash() == B4.previousHash:
        print("ERROR! Couldn't detect tampering.")
    else:
        print("Success! Tampering detected.")

    # alteração de registros

    print(B4.data)
    B4.data.num = 99999
    print(B4.data)
    if B5.previousBlock.computeHash() == B5.previousHash:
        print("ERROR! Couldn't detect tampering.")
    else:
        print("Success! Tampering detected.")





    # transactions
    print("transactions\n")

    pr1, pu1 = generate_keys()
    pr2, pu2 = generate_keys()
    pr3, pu3 = generate_keys()
    pr4, pu4 = generate_keys()

    #cria uma transação
    #na transação vai a chave publica
    #e a chave privada assina a transação
    #todos os dados da transação são assinados pela chave privada
    
    Tx0 = Tx()
    Tx0.add_input(pu1,10)
    Tx0.add_output(pu2,20)
    Tx0.sign(pr1)
    if Tx0.is_valid():
        print("Sucessooooooo\n")
    else:
        print("Fraudeee\n")
    
    '''
    Tx1 = Tx()
    Tx1.add_input(pu1, 1)
    Tx1.add_output(pu2, 1)
    Tx1.sign(pr1)
    if Tx1.is_valid():
        print("Success! Tx is valid")
    else:
        print("ERROR! Tx is invalid")

    Tx2 = Tx()
    Tx2.add_input(pu1, 2)
    Tx2.add_output(pu2, 1)
    Tx2.add_output(pu3, 1)
    Tx2.sign(pr1)

    Tx3 = Tx()
    Tx3.add_input(pu3, 1.2)
    Tx3.add_output(pu1, 1.1)
    Tx3.add_reqd(pu4)
    Tx3.sign(pr3)
    Tx3.sign(pr4)

    for t in [Tx1, Tx2, Tx3]:
        if t.is_valid():
            print("Success! Tx is valid")
        else:
            print("ERROR! Tx is invalid")

    # Wrong signatures
    Tx4 = Tx()
    Tx4.add_input(pu1, 1)
    Tx4.add_output(pu2, 1)
    Tx4.sign(pr2)

    # Escrow Tx not signed by the arbiter
    Tx5 = Tx()
    Tx5.add_input(pu3, 1.2)
    Tx5.add_output(pu1, 1.1)
    Tx5.add_reqd(pu4)
    Tx5.sign(pr3)

    # Two input addrs, signed by one
    Tx6 = Tx()
    Tx6.add_input(pu3, 1)
    Tx6.add_input(pu4, 0.1)
    Tx6.add_output(pu1, 1.1)
    Tx6.sign(pr3)

    # Outputs exceed inputs
    Tx7 = Tx()
    Tx7.add_input(pu4, 1.2)
    Tx7.add_output(pu1, 1)
    Tx7.add_output(pu2, 2)
    Tx7.sign(pr4)

    # Negative values
    Tx8 = Tx()
    Tx8.add_input(pu2, -1)
    Tx8.add_output(pu1, -1)
    Tx8.sign(pr2)

    # Modified Tx
    Tx9 = Tx()
    Tx9.add_input(pu1, 1)
    Tx9.add_output(pu2, 1)
    Tx9.sign(pr1)
    # outputs = [(pu2,1)]
    # change to [(pu3,1)]
    Tx9.outputs[0] = (pu3, 1)

    for t in [Tx4, Tx5, Tx6, Tx7, Tx8, Tx9]:
        if t.is_valid():
            print("ERROR! Bad Tx is valid")
        else:
            print("Success! Bad Tx is invalid")

    '''