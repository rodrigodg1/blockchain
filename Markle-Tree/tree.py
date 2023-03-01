import hashlib

# Create a class for the Merkle tree
class MerkleTree:
    # Initialize the class with a list of transactions
    def __init__(self, transactions):
        self.transactions = transactions
        self.past_transaction = []  # list to store the hashed transactions
        self.root = None  # initialize the root to None
        self.build()  # build the Merkle tree

    # Build the Merkle tree
    def build(self):
        # Iterate through each transaction and hash it, then add it to the list of past transactions
        for transaction in self.transactions:
            self.past_transaction.append(self.hash(transaction))

        # Build the Merkle tree using the list of hashed transactions
        self.root = self._build_merkle_tree(self.past_transaction)

    # Recursive function to build the Merkle tree
    def _build_merkle_tree(self, transactions):
        # If there is only one transaction left, return it (this is the Merkle root)
        if len(transactions) == 1:
            return transactions[0]

        # Create a list to store the next level of transactions
        next_level_transactions = []

        # Iterate through the transactions in pairs and hash them together
        for i in range(0, len(transactions) - 1, 2):
            current_transaction = transactions[i]
            next_transaction = transactions[i + 1]
            next_level_transactions.append(self.hash(current_transaction + next_transaction))

        # If there is an odd number of transactions, hash the last transaction with itself
        if len(transactions) % 2 == 1:
            next_level_transactions.append(self.hash(transactions[-1] + transactions[-1]))

        # Recursively build the Merkle tree with the next level of transactions
        return self._build_merkle_tree(next_level_transactions)

    # Hash a transaction using SHA-256
    def hash(self, transaction):
        return hashlib.sha256(transaction.encode('utf-8')).hexdigest()

    # Get the Merkle root
    def get_root(self):
        return self.root





transactions = ["Transaction 1", "Transaction 2", "Transaction 3", "Transaction 4"]
merkle_tree = MerkleTree(transactions)

print("Merkle Root:", merkle_tree.get_root())
