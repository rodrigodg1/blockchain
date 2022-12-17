from hashlib import sha256
from time import time
from flask import Flask, request, render_template

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.hash = self.get_hash()

    def get_hash(self):
        block_string = f"{self.index}{self.transactions}{self.timestamp}{self.previous_hash}"
        return sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, [], time(), "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.get_hash()
        self.chain.append(new_block)

app = Flask(__name__)

# Create the blockchain
blockchain = Blockchain()

@app.route("/", methods=["GET"])
def index():
    # Render the HTML template with the blockchain data
    blockchain_reversed = list(reversed(blockchain.chain))
    return render_template("index.html", blockchain=blockchain_reversed)

@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    # Get the transaction data from the request
    transaction_data = request.form["transaction"]

    # Create a new block with the transaction data
    new_block = Block(index=len(blockchain.chain), transactions=[transaction_data], timestamp=time(), previous_hash=blockchain.get_latest_block().hash)

    # Add the block to the blockchain
    blockchain.add_block(new_block)

    # Redirect to the index page
    return index()

if __name__ == "__main__":
    app.run(debug=True)
