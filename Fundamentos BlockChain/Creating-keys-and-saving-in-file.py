import pickle
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048,)
public_key = private_key.public_key()

#para armazenar a chave privada no arquivo
pem_private_key = private_key.private_bytes(
   encoding=serialization.Encoding.PEM,
   format=serialization.PrivateFormat.PKCS8,
   encryption_algorithm=serialization.BestAvailableEncryption(b'rodrigo')
)
f = open("private_key.pem", "wb")
f.write(pem_private_key)
f.close()


#para armazenar a chave publica no arquivo
pem_public_key = public_key.public_bytes(
   encoding=serialization.Encoding.PEM,
   format=serialization.PublicFormat.SubjectPublicKeyInfo
)
f = open("public_key.pem", "wb")
f.write(pem_public_key)
f.close()

#open private key with password
with open("private_key.pem", "rb") as key_file:
    private_key_from_file = serialization.load_pem_private_key(
        key_file.read(),
        password=b'rodrigo',
    )


#open public key
with open("public_key.pem", "rb") as key_file:
    public_key_from_file = serialization.load_pem_public_key(
        key_file.read()
    )

print(private_key_from_file)
print(public_key_from_file)