import socket
import sys
import os
import rsa
import pickle

HOST = "localhost"
PORT = 8050
BUF_SIZE = 1024
DOWNLOAD_DIR = "test"


mfile = open("keyInfo", "rb+")
keys = pickle.load(mfile)
K_A_pub = keys["K_A_pub"]





sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((HOST, PORT))
    print("Connected to A")
except Exception as e:
    print("cannot connect to server:", e, file=sys.stderr)

down_file = os.path.join(DOWNLOAD_DIR, "FileGotFromA")


rcvd = []

while True:
    rec = sock.recv(BUF_SIZE)
    rcvd.append(rec)

sock.close()

time, Hash = None, None
# time = rcvd[i:j]
# hash = rcvd[i:j]

print("Timestamp is:", time)

# calculate hash and verify it

# decrypt file contents one by one and write to new file

down_file = os.path.join(DOWNLOAD_DIR, 'fileReceivedFromA')
with open(down_file, 'wb') as output:
    
    for content in rcvd:    #note that rcvd also contain time and hash so they need to be removed
        decrypted = rsa.decrypt(content, K_A_pub)
        output.write(decrypted)

print('Success!')