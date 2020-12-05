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

    '''

    # transactions
    # para representar as transações, deve-ser ter uma entrar Input e uma saida Output,
    # chave publica para a conta origem e chave publica para a conta destino
    # quem inicia a transação, deve-ser assina-la com a chave privada
    print("\n\nTRANSACTIONS\n")

    pr1, pu1 = generate_keys()
    pr2, pu2 = generate_keys()
    pr3, pu3 = generate_keys()

    Tx1 = Tx()
    Tx1.add_input(pu1, 1)
    Tx1.add_input(pu1, 1)
    Tx1.add_output(pu2, 1)
    Tx1.sign(pr1)

    if Tx1.is_valid():
        print("Success! Tx is valid")

    # armazena a transação no arquivo
    savefile = open("tx.dat", "wb")
    pickle.dump(Tx1, savefile)
    savefile.close()

    # carrega a transação
    loadfile = open("tx.dat", "rb")
    newTx = pickle.load(loadfile)

    if newTx.is_valid():
        print("Sucess! Loaded tx is valid")
    loadfile.close()

    # bloco genesis nao tem anterior (None)
    root = TxBlock(None)
    root.addTx(Tx1)

    # transacao valida
    Tx2 = Tx()
    Tx2.add_input(pu2, 1.1)
    Tx2.add_output(pu3, 1)
    Tx2.sign(pr2)
    root.addTx(Tx2)

    # cria um segundo bloco da cadeia
    # referenciando o genesis como anterior
    B1 = TxBlock(root)
    Tx3 = Tx()
    Tx3.add_input(pu3, 1.1)
    Tx3.add_output(pu1, 1)
    Tx3.sign(pr3)
    B1.addTx(Tx3)

    # transacao valida
    Tx4 = Tx()
    Tx4.add_input(pu1, 1)
    Tx4.add_output(pu2, 1)
    Tx4.add_reqd(pu3)
    Tx4.sign(pr1)
    Tx4.sign(pr3)
    B1.addTx(Tx4)

    Tx0 = Tx()
    Tx0.add_input(pu3, 10)
    Tx0.add_output(pu2, 9)
    # transacao valida
    Tx0.sign(pr3)

    # transacao invalida
    # Tx0.sign(pr2)
    B1.addTx(Tx0)

    Btest = TxBlock(B1)
    TxTEST = Tx()
    TxTEST.add_input(pu3, 1.1)
    TxTEST.add_output(pu1, 1)
    TxTEST.sign(pr3)
    Btest.addTx(TxTEST)

    savefile = open("block.dat", "wb")
    pickle.dump(B1, savefile)
    savefile.close()

    loadfile = open("block.dat", "rb")
    load_B1 = pickle.load(loadfile)

    # example blockchain
    blockchain = Blockchain("My-Chain")

    # faz a contagem das transações válidas no bloco
    for block in [root, B1, Btest]:
        print(
            f"\nValid transactions on block {block.id_block} : {block.count_valid_transactions()} ")

# verifica os blocos criados aqui e tbm dos arquivos
    for b in [root, B1, load_B1, load_B1.previousBlock, Btest]:
        print(f"\nblock {b.id_block}")
        if b.is_valid():
            print("Success! Valid block")
            print("Inserting into blockchain...")
            blockchain.add_block(b)
        else:
            print("ERROR! Bad block")

    # mostra a quantidade de blocos na cadeia
    print(f"\n\nCount block into blockchain: {blockchain.count_blocks}")

    '''
    print("\n\n")
    B2 = TxBlock(B1)
    Tx5 = Tx()
    Tx5.add_input(pu3, 1)
    Tx5.add_output(pu1, 100)
    Tx5.sign(pr3)

    print("Transaction 5 valid ?: ", Tx5.is_valid())

    B2.addTx(Tx5)

    load_B1.previousBlock.addTx(Tx4)
    for b in [B2, load_B1]:
        if b.is_valid():
            print ("ERROR! Bad block verified.")
        else:
            print ("Success! Bad blocks detected")  

    '''
