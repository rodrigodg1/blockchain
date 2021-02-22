
from bitcoin import *

#gerando chave privada
my_private_key = random_key()

#gerando chave publica (é feito a partir da chave privada)
my_public_key = privtopub(my_private_key)

print(f"Private Key: {my_private_key}")
print(f"Public Key: {my_public_key}")



# e com a chave pública, geramos o endereço (Address)
my_bitcoin_address = pubtoaddr(my_public_key)
print(f"My bitcoin address: {my_bitcoin_address} ")
