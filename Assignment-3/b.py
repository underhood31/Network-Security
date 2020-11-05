import socket
import rsa


def extractPubKey(res = "Hey"):
    idx1 = res.find("e")
    idx2 = res.find("n")
    idx3 = res.find("Res")
    k_e = res[idx1+1:idx2]
    k_n = res[idx2+1:idx3]
    return rsa.PublicKey(n= k_n, e= k_e)

KpubPKDA = None # rsa.PublicKey object read from a file

# Establish connection with PKDA
s = socket.socket()

host = socket.gethostname()
port = 12346

s.connect((host,port))

# send req to PKDA

# response from PKDA
response = s.recv(1024)
response = rsa.decrypt(response, KpubPKDA)
KpubA = extractPubKey(response)

s.close()
# accept connection from A

# communicate with A

