import socket
import sys
import os
import hashlib
import pickle
import datetime
import rsa

HOST = "localhost"
PORT = 8050
BUF_SIZE = 245
DOWNLOAD_DIR = "TimeStampDirectory"

mfile = open("Server_keyInfo", "rb+")
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
rcvStr=b''
# while True:
#     print(len(rcvd))
#     rec = conn.recv(BUF_SIZE)
#     if not rec:
#         break

#     rcvd.append(rec)

# conn.close()

while True:
    
    rec = conn.recv(BUF_SIZE)
    if not rec:
        break
    rcvStr += rec


conn.close()

i = 82
while True:
    i = rcvStr.find(b"||")
    if (i==-1):
        break
    rcvd.append(rcvStr[:i])
    rcvStr = rcvStr[i+len('||'):]


print("Done receiving from A")

currTime = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
rcvd.append(currTime.encode('utf-8'))
#Add time to array. It will be of fixed length so break into 1024 size chunks and add to array.
print("Length:", len(rcvd))
hasher = hashlib.sha3_512()

for idx,i in enumerate(rcvd):
    # print(idx)
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
    # print(indx)
    conn.sendall(i)
    conn.sendall(b"||")
print("Done sending to B")
conn.close()
