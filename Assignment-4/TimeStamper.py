import socket
import sys
import os
import hashlib
import pickle


HOST = "localhost"
PORT = 8050
BUF_SIZE = 4096
DOWNLOAD_DIR = "test"


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
    rec = sock.recv(BUF_SIZE)
    
    if not rec:
        break

    rcvd.append(rec)

conn.close()
#Add time to array. It will be of fixed length so break into 1024 size chunks and add to array.

hasher = hashlib.sha3_512()

for i in rcvd:
    hasher.update(i)

hashVal = hasher.digest()

# Break hashVal to 1024 size chunks and add to array




# add waiting condition and B's download request condition

conn, addr = sock.accept()
print("Connected by", str(addr))

for i in rcvd:
    conn.sendall(i)

conn.close()
