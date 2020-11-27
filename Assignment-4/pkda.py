import socket
import sys
import os
import hashlib
import pickle
import rsa

mfile = open("pkda_keyInfo", "rb+")
keys = pickle.load(mfile)
K_A_pub = keys["K_A_pub"]
K_pkda_pri = keys["K_pkda_pri"]
K_server_pub = keys["K_Server_pub"]


keyA  =  pickle.dumps(K_A_pub)
hasher =  hashlib.sha3_512()
hasher.update(keyA)
hashA = hasher.digest()
# print("HAshA:", hashA)
keyServer  =  pickle.dumps(K_server_pub)
hasher =  hashlib.sha3_512()
hasher.update(keyServer)
hashServer = hasher.digest()

hashA = rsa.encrypt(hashA, K_pkda_pri)
hashServer = rsa.encrypt(hashServer, K_pkda_pri)
msgTosend = keyA + b'Hsh' + hashA + b'Srv' + keyServer + b'Hsh' + hashServer
# print(hashA)
 
HOST = "localhost"
PORT = 8082

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

conn, addr = sock.accept()
print("Connected by", str(addr))

conn.send(msgTosend)

conn.close()
