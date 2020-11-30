from libs import *



def generate_keys():
    #gera a chave privada
    private = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    ) 
    #a partir da chave private, é possível gerar a chave pública   
    public = private.public_key()
    return private, public

def sign(message, private):
    #assina a mensagem que recebeu por parametro
    ## assinatura realizada com a chave privada
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

#para verificar, nao é necessario a chave privada
# isso é feito de forma rápida com a chave pública
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
    

if __name__ == '__main__':
    pr,pu = generate_keys()
    print("Private Key: ",pr)
    print("\nPublic key: ",pu)

    message = "This is a secret message"
    sig = sign(message, pr)
    print("\nSig msg: ", sig)
    correct = verify(message, sig, pu)
    print("Correct: ", correct)

    if correct:
        print("Success! Good sig")
    else:
        print ("ERROR! Signature is bad")

    pr2, pu2 = generate_keys()

    sig2 = sign(message, pr2)

    #porem verifica se a mensagem está correta com a chave publica 1 (outra chave)
    correct= verify(message, sig2, pu)
    if correct:
        print("ERROR! Bad signature checks out!")
    else:
        print("Success! Bad sig detected")




    badmess = message + "Q"
    correct= verify(badmess, sig, pu)
    if correct:
        print("ERROR! Tampered message checks out!")
    else:
        print("Success! Tampering detected")
    
    
    
        
    
