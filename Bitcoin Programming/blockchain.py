# import blockchain library
#essa lib, permite consultar informações sobre o bitcoin
from blockchain import exchangerates
from blockchain import statistics
from blockchain import blockexplorer

# retorna o valor do bitcoin em cada moeda
ticker = exchangerates.get_ticker()

#mostra o valor do bitcoin a cerca de 15 min
for k in ticker:
    print(k, ticker[k].p15min)
    
    
# Converte o valor de uma moeda para o respectivo valor em bitcoin
btc = exchangerates.to_btc('EUR', 100)
print(f"\n100 euros in Bitcoin: {btc}")





#utilizando a lib statistics
stats = statistics.get()
# total de bitcoin minerados
print("Bitcoin mined: %s\n" % stats.btc_mined)


# valor do bitcoin em USD
print(f"Bitcoin market price USD: {stats.market_price_usd}\n" )








#utilizando a lib blockexplorer
# retorna um bloco em particular
block = blockexplorer.get_block('0000000000000000002e90b284607359f3415647626447643b9b880ee00e41fa')

#pode-se obter informações desse bloco em particular
print("Block Fee: %s\n" % block.fee)
print("Block size: %s\n" % block.size)
print("Block transactions: %s\n" % block.transactions)






#ultimo bloco
latest_block = blockexplorer.get_latest_block()


