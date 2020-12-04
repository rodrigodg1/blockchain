from libs import *
from hashing import *
from signatures import *


class someClass:
    string = None
    num = 328965

    def __init__(self, mystring):
        self.string = mystring

    def __repr__(self):
        return self.string + "^^^" + str(self.num)


class CBlock:
    data = None
    previousHash = None
    previousBlock = None

    def __init__(self, data, previousBlock):
        self.data = data
        self.previousBlock = previousBlock
        if previousBlock != None:
            self.previousHash = previousBlock.computeHash()

    def computeHash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.data), 'utf8'))
        digest.update(bytes(str(self.previousHash), 'utf8'))
        return digest.finalize()
