import socket
import rsa
import pickle

print("Public Key Distribution Authority is active now")

mfile = open("pkda_keyInfo", "rb+")
availableKeys = pickle.load(mfile)

KpubA = availableKeys['k_pub_a']
KpubB = availableKeys['k_pub_b']
KpriPKDA = availableKeys['k_pri_pkda']

key_to_return = {12345:KpubA , 12346: KpubB}

# accept connection from A and send pub key of B
sktA = socket.socket()
host = socket.gethostname()
portA = 12345
sktA.bind((host, portA))
sktA.listen(2)

while True:
    (clientAskt , clientAaddr) = sktA.accept()
    print("Connected to ",clientAskt)
    req_unprocessed=clientAskt.recv(1024)
    req = req_unprocessed.decode('utf-8').split("|")
    reqPort=int(req[0][2:],16)
    print("Public key requested for:", reqPort)
    
    #From a premade dictionary get the public key wrt reqPort 

    #Now send the requested public key with T1 appended
    msg = rsa.encrypt((pickle.dumps(key_to_return[reqPort]) + "|".encode('utf-8') + req_unprocessed), KpriPKDA)
    clientAskt.send(msg)
    clientAskt.close()



