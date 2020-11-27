import socket
import sys
import os
import rsa
import pickle

HOST = "localhost"
PORT = 8050
BUF_SIZE = 1024
mfile = open("A_keyInfo", "rb+")
keys = pickle.load(mfile)
K_A_pri = keys["K_A_pri"]

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


with open(file_name,'rb') as output:
    while True:
        data = output.read(BUF_SIZE)
        print("Data Read:", data)
        if not data:
            break
        data = rsa.encrypt(data, K_A_pri)
        sock.sendall(data)
        total_sent += len(data)

    print("finished sending", total_sent, "bytes")

sock.close() # close listener


#####
