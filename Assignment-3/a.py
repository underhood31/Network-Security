import socket
import rsa
import time
import random
import sys
import pickle

#Globals(To be read from a file)
portB=12346
ABport=12347
MIN_DELTA=1 #min delta time should be 1 sec
mfile = open("a_keyInfo", "rb+")
availableKeys = pickle.load(mfile)

KprivA= availableKeys["k_pri_a"]
KpubPKDA = availableKeys["k_pub_pkda"]

def extractPubKey(res):
    idx = res.find(b"|")
    return pickle.loads(res[:idx]),res[idx+1:]
    


print("Press Enter to start client A...")
input()

# Establish connection with PKDA
print("--> Establish connection with PKDA")
s = socket.socket()

host = socket.gethostname()
port = 12345
s.connect((host,port))

# send request to PKDA(request will contain the port number of B)
print("--> Request sent to PKDA(request will contain the port number of B)")
initMessage=hex(portB)+"|"+hex(int(time.time()))
s.send(initMessage.encode('utf-8'))

# response from PKDA
print("--> Encrypted response received containg public key of B")
response = s.recv(1024)
response = rsa.decrypt(response, KpubPKDA)
KpubB,appended_res = extractPubKey(response)
print("--> Received public Key of B", KpubB)
appended_res=appended_res.decode('utf-8').split('|')
got_time=int(appended_res[1],16)

#verify delta time
print("--> Verifying delt time in response")
delta_time=time.time()-got_time
if delta_time>MIN_DELTA:
	print("!!! Got delayed response, exiting")
	sys.exit(1)
else:
	print("--> Response time verified")

s.close()

s = socket.socket()

# establish connection with B
s.connect((host,ABport))


# communicate with B
print("--> Communication with B initiated")
# 1. send message to B
print("--> Sending encrypted request to B")
N1=random.getrandbits(64)
IdA=port
BMessage=hex(IdA)+"|"+hex(N1)
BMessage=rsa.encrypt(BMessage.encode('utf-8'),KpubB)
s.send(BMessage)

# 2. Receive from B
print("--> Receiving Encrypted response from B")
Bget=rsa.decrypt(s.recv(1024),KprivA)
Bget=Bget.decode('utf-8')
print("Received from B:", Bget)
Bget=Bget.split('|')
if(int(Bget[0][2:],16)!=N1):
	print("!!! Response from B cannot be verified")
	sys.exit(1)
else:
	print("--> Response N1 from B verified")
# 3. Final message to B
print("--> Sending encrpted N2 to B")
BMessage=rsa.encrypt(Bget[1].encode('utf-8'),KpubB)
s.send(BMessage)

#initialize chat client
print("--> Chat client initialized <--")
while(True):
	toSend=input("Enter message: ").encode('utf-8')
	toSend=rsa.encrypt(toSend,KpubB)
	s.send(toSend)
	got=s.recv(1024)
	print("----> Got message from B, decrypting...")
	print("recv: ", rsa.decrypt(got,KprivA).decode('utf-8'))
	res=input("Wanna continue??(Y/n)") 
	if res=='N' or res=='n':
		s.send(rsa.encrypt("<--END-->".encode("utf-8"),KpubB))
		break

#ending connection
s.close()
