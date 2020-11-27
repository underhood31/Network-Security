import socket
import sys
import os
import rsa
import pickle

HOST = "localhost"
PORT = 8050
BUF_SIZE = 245
mfile = open("A_keyInfo", "rb+")
keys = pickle.load(mfile)
K_A_pri = keys["K_A_pri"]
DIR="Adir"

#############
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((HOST, PORT))
    print("Connected to Server")
except Exception as e:
    print("cannot connect to server:", e, file=sys.stderr)


file_name = input("\nFile to send: ")
print("Sending File:", file_name)

total_sent = 0

# fn=rsa.encrypt(file_name.encode('utf-8'),K_A_pri)
# print(fn)
# sock.send(fn)
sock.send((file_name.encode('utf-8')))
sock.sendall(b'||')

with open(DIR+"/"+file_name,'rb') as output:
    j=0
    while True:
        data = output.read(BUF_SIZE)
        # print("Data Read:", data)
        if not data:
            break

        data = rsa.encrypt(data, K_A_pri)
        # if j<20:
        # 	print(j)
        # 	print(data)
        j+=1
        sock.sendall(data)
        sock.sendall(b'||')
        total_sent += len(data)

    print("finished sending", total_sent, "bytes")

sock.close() # close listener


#####
