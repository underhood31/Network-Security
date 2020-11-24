import socket
import sys
import os
import hashlib
import pickle
import datetime
import rsa

HOST = "localhost"
PORT = 8050
BUF_SIZE = 4096
DOWNLOAD_DIR = "test"

mfile = open("keyInfo", "rb+")
keys = pickle.load(mfile)
K_Server_pri = keys["K_Server_pri"]

## receive connection request from A

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
keep_going = 1

# add waiting condition and A's upload request condition
conn, addr = sock.accept()
print("Connected by", str(addr))

rcvd = []

while True:
    print(len(rcvd))
    rec = conn.recv(BUF_SIZE)
    
    if not rec:
        break

    rcvd.append(rec)

conn.close()

print("Done receiving from A")

currTime = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
rcvd.append(currTime.encode())
#Add time to array. It will be of fixed length so break into 1024 size chunks and add to array.
print("Length:", len(rcvd))
hasher = hashlib.sha3_512()

for idx,i in enumerate(rcvd):
    print(idx)
    hasher.update(i)

hashVal = hasher.digest()
hashVal = rsa.encrypt(hashVal, K_Server_pri)
rcvd.append(hashVal)
# print("rcvd", rcvd)
# Break hashVal to 1024 size chunks and add to array




# add waiting condition and B's download request condition

conn, addr = sock.accept()
print("Connected by", str(addr))

for indx, i in enumerate(rcvd):
    print(indx)
    conn.sendall(i)
    conn.sendall(b"manavBimarHai")

conn.close()
