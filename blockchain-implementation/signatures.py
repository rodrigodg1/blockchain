from libs import *


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
    
    
    
        
    
