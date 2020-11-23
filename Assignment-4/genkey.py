import pickle

import rsa

keysz = 2048

K_pub_A, K_pri_A = rsa.newkeys(keysz)


pkdaFile = open('keyInfo', 'wb+')

pickle.dump({"K_A_pri": K_pub_A, "K_A_pub": K_pri_A}, pkdaFile)

pkdaFile.close()
