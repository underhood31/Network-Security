import socket
import rsa
import time
import random
import sys

#Globals(To be read from a file)
portB=12346
ABport=99999
KprivA=???

def extractPubKey(res = "Hey"):
    idx1 = res.find("e")
    idx2 = res.find("n")
    idx3 = res.find("Res")
    k_e = res[idx1+1:idx2]
    k_n = res[idx2+1:idx3]
    return rsa.PublicKey(n= k_n, e= k_e)

KpubPKDA = None # rsa.PublicKey object read from a file

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
response = rsa.decrypt(response, KpubPKDA).decode('utf-8')
KpubB = extractPubKey(response)
s.close()

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
