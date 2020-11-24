import pickle

import rsa

keysz = 2048

K_pub_A, K_pri_A = rsa.newkeys(keysz)
K_pub_Server, K_pri_Server = rsa.newkeys(keysz)


pkdaFile = open('keyInfo', 'wb+')

pickle.dump({"K_A_pri": K_pub_A, "K_A_pub": K_pri_A, "K_Server_pri": K_pub_Server, "K_Server_pub": K_pri_Server}, pkdaFile)
# pickle.dump({}, pkdaFile)


pkdaFile.close()
