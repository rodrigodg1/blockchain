
#Signatures module

def generate_keys():
    
    private="aa"
    public="bb"

    return private, public


def sign(message,private):
    sig="joajdsdjad38472$%#"
    return sig


def verify(message,sign,public):
    return False

if __name__ == '__main__':
    pr,pu = generate_keys()
    message = b"Secret message, hello !"
    sig = sign(message,pr)
    correct = verify(message,sig,pub)
    








