
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


#endereço com multiplas assinaturas = está associado a mais de uma chave privada

#1 - Criar as chaves privadas
my_private_key1 = random_key()
my_private_key2 = random_key()
my_private_key3 = random_key()

#2 - Criar as chaves publicas a partir das privadas
my_public_key1 = privtopub(my_private_key1)
my_public_key2 = privtopub(my_private_key2)
my_public_key3 = privtopub(my_private_key3)


#3 - Assim, pode-se criar a multipla assinatura e um endereço
my_multi_sig = mk_multisig_script(my_private_key1,my_private_key2,my_private_key3,2,3)
my_multi_address = scriptaddr(my_multi_sig)


print(f"My multi signature address: {my_multi_address}")



#valid bitcoin_address (retiado de Blockchain.info)
valid_bitcoin_address = "1794nFZx1qegzYxbtUMMyMc9Eq8nsPFnKW"
#é possivel ver o histórico de transações
print(history(valid_bitcoin_address))











