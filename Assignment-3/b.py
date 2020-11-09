import socket
import rsa
import time
import random
import sys
import pickle
import concurrent.futures
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

def getPubkeyFromPKDA(IdA):
	# Establish connection with PKDA
	print("--> Getting public key of",IdA,"from PKDA")
	s = socket.socket()
	port = 12345
	s.connect((host,port))

	# send req to PKDA(contains port of B)
	initMessage=hex(IdA)+"|"+hex(int(time.time()))
	s.send(initMessage.encode('utf-8'))

	# response from PKDA
	response = s.recv(1024)
	response = rsa.decrypt(response, KpubPKDA)
	pubkey = extractPubKey(response)
	print("--> Received public Key of A:", pubkey)
	s.close()

	return pubkey
    
host = socket.gethostname()


# accept connection from A
peer = socket.socket()
peer.bind((host, ABport))
peer.listen(20)
peerSkt , peerAaddr = peer.accept()
print("--> Connection request from ",peerSkt)
req_unprocessed=rsa.decrypt(peerSkt.recv(1024),KprivB)
req = req_unprocessed.decode('utf-8').split("|")
reqPort=int(req[0][2:],16)
N1=req[1]
print("--> Public key requested for:", reqPort)


# KpubA=None
# with concurrent.futures.ThreadPoolExecutor() as executor:
#     future = executor.submit(getPubkeyFromPKDA, reqPort)
#     KpubA = future.result()

KpubA=getPubkeyFromPKDA(reqPort)




# communicate with A
# 1. send message
print("--> Sending encrypted N1||N2 message to A")
N2=random.getrandbits(64)
N2_tosend=hex(N2)
AMessage=(N1+"|"+N2_tosend).encode('utf-8')
AMessage=rsa.encrypt(AMessage,KpubA)
peerSkt.send(AMessage)

# 2. Evaluate reply
print("--> Received encrypted N2 from A, evaluating reply")
getA=peerSkt.recv(1024)
getA=rsa.decrypt(getA,KprivB).decode('utf-8')
if(int(getA[2:],16)==N2):
	print("--> Success")
else:
	print("!!! Failed")

print("--> Chat client initialized <--")
count=0
while(True):
	rec=rsa.decrypt(peerSkt.recv(1024),KprivB).decode('utf-8')
	if(rec=="<--END-->"):
		break
	else:
		print("Got:", rec)
		toSend="Got-it "+str(count)
		toSend=rsa.encrypt(toSend.encode('utf-8'),KpubA)
		peerSkt.send(toSend)
	count+=1

peer.close()


