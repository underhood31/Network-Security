import socket
import rsa
import time
import random
import sys
import pickle

#Globals(To be read from a file)
portB=12346
ABport=12347

mfile = open("a_keyInfo", "rb+")
availableKeys = pickle.load(mfile)

KprivA= availableKeys["k_pri_a"]
KpubPKDA = availableKeys["k_pub_pkda"]

def extractPubKey(res):
    idx = res.find(b"Res")
    return pickle.loads(res[:idx])
    

# Establish connection with PKDA
s = socket.socket()

host = socket.gethostname()
port = 12345
s.connect((host,port))

# send request to PKDA(request will contain the port number of B)
initMessage=hex(portB)+"|"+hex(int(time.time()))
s.send(initMessage.encode('utf-8'))

# response from PKDA
response = s.recv(1024)
response = rsa.decrypt(response, KpubPKDA)
KpubB = extractPubKey(response)
print("Received public key of B", KpubB)
s.close()

s = socket.socket()

# establish connection with B
s.connect((host,ABport))


# communicate with B
# 1. send message to B
N1=random.getrandbits(64)
IdA=port
BMessage=hex(IdA)+"|"+hex(N1)
BMessage=rsa.encrypt(BMessage.encode('utf-8'),KpubB)
s.send(BMessage)

# 2. Receive from B
Bget=rsa.decrypt(s.recv(1024),KprivA)
Bget=Bget.decode('utf-8')
Bget=Bget.split('|')
if(int(Bget[0][2:],16)!=N1):
	print("Response from B cannot be verified")
	sys.exit(1)
# 3. Final message to B
BMessage=rsa.encrypt(Bget[1].encode('utf-8'),KpubB)
s.send(BMessage)

#ending connection
s.close()
