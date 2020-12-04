from libs import *



def hashing(message):

    digest = hashes.Hash(hashes.SHA256(),backend=default_backend())

    digest.update(message)
    msg1_hash = digest.finalize()

    return msg1_hash

#hash gerado é completamente diferente apenas com uma mudança

