import socket
import rsa
import pickle
# Key info with PKDA (Better if we read this from a file and write a script to generate that file using rsa.newkey(1024))

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
    req = clientAskt.recv(1024).decode('utf-8').split("|")
    reqPort=int(req[0][2:],16)
    print("Public key requested for:", reqPort)
    
    #From a premade dictionary get the public key wrt reqPort 

    #Now send the requested public key with T1 appended
    msg = rsa.encrypt((pickle.dumps(key_to_return[reqPort]) + bytes("Res:", "ascii")), KpriPKDA)
    clientAskt.send(msg)
    clientAskt.close()
    # break

# # accept connection from B and send pub key of A

# sktB = socket.socket()
# portB = 12346
# sktB.bind((host, portB))
# sktB.listen(5)
# while True:
#     (clientBskt , clientBaddr) = sktB.accept()
#     msg = "Connected to B"
#     req = clientBskt.recv(1024).decode()
#     msg = rsa.encrypt(("e:"+str(KpubA['e']) + "n:"+str(KpubA['n']) + "Res:"+ req).encode(), myPrivateKey)
#     clientBskt.send(msg)
#     clientBskt.close()
#     break

# print("Done sending keys")



