import socket
import rsa

# Key info with PKDA (Better if we read this from a file and write a script to generate that file using rsa.newkey(1024))

KpubA = {'e': 2, 'n': 4}    
KpubB = ()
KpriPKDA = {'d': 2, 'p': 3, 'q': 4}


myPrivateKey = rsa.PrivateKey(n=KpriPKDA['n'], e=KpriPKDA['e'] , d=KpriPKDA['d'], p=KpriPKDA['p'], q=KpriPKDA['q'])


# accept connection from A and send pub key of B
sktA = socket.socket()
host = socket.gethostname()
portA = 12345
sktA.bind((host, portA))
sktA.listen(5)

while True:
    (clientAskt , clientAaddr) = sktA.accept()
    print("Connected to A")
    req = clientAskt.recv(1024).decode()
    msg = rsa.encrypt(("e:"+str(KpubB['e']) + "n:"+str(KpubB['n']) + "Res:"+ req).encode(), myPrivateKey)
    clientAskt.send(msg)
    clientAskt.close()
    break

# accept connection from B and send pub key of A

sktB = socket.socket()
portB = 12346
sktB.bind((host, portB))
sktB.listen(5)
while True:
    (clientBskt , clientBaddr) = sktB.accept()
    msg = "Connected to B"
    req = clientBskt.recv(1024).decode()
    msg = rsa.encrypt(("e:"+str(KpubA['e']) + "n:"+str(KpubA['n']) + "Res:"+ req).encode(), myPrivateKey)
    clientBskt.send(msg)
    clientBskt.close()
    break

print("Done sending keys")



