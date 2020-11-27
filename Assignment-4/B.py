import socket
import sys
import os
import rsa
import pickle
import hashlib
import rsa

HOST = "localhost"
PORT = 8050
BUF_SIZE = 1024
DOWNLOAD_DIR = "test"


mfile = open("B_keyInfo", "rb+")
keys = pickle.load(mfile)
K_pkda_pub = keys["K_pkda_pub"]

# receive required keys from pkda

port2 = 8082
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# try:
sock.connect((HOST, port2))
print("Connected to PKDA")
# except Exception as e:
#     print("cannot connect to pkda:", e, file=sys.stderr)

stringIn = b''

while True:
    
    rec = sock.recv(BUF_SIZE)
    if not rec:
        break
    stringIn += rec
    
sock.close()


i1 = stringIn.find(b'Hsh')
K_A_pub = stringIn[:i1]
i2 = stringIn.find(b'Srv')
K_A_hsh = stringIn[i1+3:i2]
i3 = stringIn.find(b'Hsh', i2+1)
K_Server_pub = stringIn[i2+3:i3]
K_Server_hsh = stringIn[i3+3:]
# print("Hash:", K_A_hsh)

K_A_hsh = rsa.decrypt(K_A_hsh, K_pkda_pub)

K_Server_hsh = rsa.decrypt(K_Server_hsh, K_pkda_pub)

hasher =  hashlib.sha3_512()
hasher.update(K_A_pub)
hashA = hasher.digest()
if (hashA == K_A_hsh):
    print('Public Key of A verified')

hasher =  hashlib.sha3_512()
hasher.update(K_Server_pub)
hashA = hasher.digest()
if (hashA == K_Server_hsh):
    print('Public Key of Server verified')

K_A_pub = pickle.loads(K_A_pub)
K_Server_pub = pickle.loads(K_Server_pub)
input()
# except:
#     print("Key Receiving failed")


##############
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((HOST, PORT))
    print("Connected to Server")
except Exception as e:
    print("cannot connect to server:", e, file=sys.stderr)

down_file = os.path.join(DOWNLOAD_DIR, "FileGotFromA")


rcvd = []

rcvStr= b''
while True:
    
    rec = sock.recv(BUF_SIZE)
    if not rec:
        break
    # print("Got:", rec)
    rcvStr += rec
    # rcvd.append(rec)


sock.close()

i = 82
while True:
    i = rcvStr.find(b"manavBimarHai")
    if (i==-1):
        break
    rcvd.append(rcvStr[:i])
    rcvStr = rcvStr[i+13:]

time, Hash = rcvd[-2], rcvd[-1]
time = time.decode()

print("Timestamp is:", time)

# print(rcvd)
Hash = rsa.decrypt(Hash, K_Server_pub)

hasher = hashlib.sha3_512()

for i in rcvd[:-1]:
    hasher.update(i)

hashVal = hasher.digest()

if hashVal == Hash:
    print("Ho gya match")
else:
    print("Nahi hua")

# calculate hash and verify it

# decrypt file contents one by one and write to new file

down_file = os.path.join(DOWNLOAD_DIR, 'fileReceivedFromA')
with open(down_file, 'wb') as output:
    
    for content in rcvd[:-2]:    #note that rcvd also contain time and hash so they need to be removed
        decrypted = rsa.decrypt(content, K_A_pub)
        output.write(decrypted)

print('Success!')