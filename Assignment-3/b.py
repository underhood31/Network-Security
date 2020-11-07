import socket
import rsa
import time
import random
import sys
import pickle


#Globals(To be read from a file)
portA=12345
ABport=12347

mfile = open("b_keyInfo", "rb+")
availableKeys = pickle.load(mfile)

KprivB= availableKeys["k_pri_b"]
KpubPKDA = availableKeys["k_pub_pkda"]


def extractPubKey(res):
    idx = res.find(b"Res")
    return pickle.loads(res[:idx])
    


host = socket.gethostname()


# Establish connection with PKDA
s = socket.socket()
port = 12345
s.connect((host,port))

IdA = 12345
# send req to PKDA(contains port of B)
initMessage=hex(IdA)+"|"+hex(int(time.time()))
s.send(initMessage.encode('utf-8'))

# response from PKDA
response = s.recv(1024)
response = rsa.decrypt(response, KpubPKDA)
KpubA = extractPubKey(response)
print("Received public Key of A", KpubA)
s.close()

# accept connection from A
peer = socket.socket()
peer.bind((host, ABport))

peer.listen(5)
peerSkt , peerAaddr = peer.accept()

getA=rsa.decrypt(peer.recv(1024),KprivB).decode('utf-8').split("|")
IdA=getA[0]
N1=getA[1]


# communicate with A
# 1. send message
N2=hex(random.getrandbits(64))
AMessage=(N1+N2).encode('utf-8')
AMessage=AMessage.encrypt(AMessage,KpubA)
peerSkt.send(AMessage)

# 2. Evaluate reply
getA=peer.recv(1024)
getA=rsa.decrypt(getA,KprivB).decode('utf-8')
if(int(getA[2:],16)==N2):
	print("Success")
else:
	print("Failed")

peer.close()


