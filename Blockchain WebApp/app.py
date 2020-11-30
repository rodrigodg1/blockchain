import datetime
import hashlib
import json
from flask import Flask, jsonify,render_template,request,redirect,session,flash

class Blockchain:

    def __init__(self):
        self.chain = []
        #blockchain hipotetico, que recebe uma pessoa origem e outra destino e um quantidade para transferencia entre elas
        self.create_block(proof = 1, previous_hash = '0', origem = '', destino='', valor='')

    def create_block(self, proof, previous_hash,origem,destino,valor):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'origem': origem,
                 'destino': destino,
                 'valor': valor}
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True


app = Flask(__name__)


blockchain = Blockchain()
lista = []

@app.route('/index')
@app.route('/')
def index():

    return render_template('lista.html',titulo="Transações",
    transacoes=lista)



@app.route('/novo')
def novo():
    
    return render_template('novo.html', titulo='Nova Transação')




#responsavel por realizar a mineracao do bloco, e acrecentar no blockchain
@app.route('/mine_block', methods = ['POST'])
def mine_block():

    origem = request.form['origem']
    destino = request.form['destino']
    valor = request.form['valor']


    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash,origem,destino,valor)
    response = {'message': 'Parabens voce acabou de minerar um bloco!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}

    lista.append(block)

    #return jsonify(response), 200
    return redirect('/')








@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message' : ' Tudo certo, o blockchain e valido '}
    else:
        response = {'message' : ' O blockchain nao e valido '}
    return jsonify(response), 200

app.run(host='0.0.0.0',debug=True)