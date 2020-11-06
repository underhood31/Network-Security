import socket
import rsa

#Globals(To be read from a file)
portA=12345
ABport=99999
KprivB=???

def extractPubKey(res = "Hey"):
    idx1 = res.find("e")
    idx2 = res.find("n")
    idx3 = res.find("Res")
    k_e = res[idx1+1:idx2]
    k_n = res[idx2+1:idx3]
    return rsa.PublicKey(n= k_n, e= k_e)

KpubPKDA = None # rsa.PublicKey object read from a file


peer = socket.socket()
host = socket.gethostname()

# accept connection from A
peer.connect((host,portA))
getA=rsa.decrypt(peer.recv(1024),KprivB).decode('utf-8').split("|")
IdA=getA[0]
N1=getA[1]

# Establish connection with PKDA
s = socket.socket()
port = 12346
s.connect((host,port))

# send req to PKDA(contains port of B)
initMessage=hex(IdA)+"|"+hex(int(time.time()))
s.send(initMessage.encode('utf-8'))

# response from PKDA
response = s.recv(1024)
response = rsa.decrypt(response, KpubPKDA)
KpubA = extractPubKey(response)
s.close()


# communicate with A
# 1. send message
N2=hex(random.getrandbits(64))
AMessage=(N1+N2).encode('utf-8')
AMessage=AMessage.encrypt(AMessage,KpubA)
peer.send(AMessage)

# 2. Evaluate reply
getA=peer.recv(1024)
getA=rsa.decrypt(getA,KprivB).decode('utf-8')
if(int(getA[2:],16)==N2):
	print("Success")
else:
	print("Failed")

peer.close()


