import pickle

import rsa

keysz = 2048
keysz2 = 4096


K_pub_A, K_pri_A = rsa.newkeys(keysz)
K_pub_Server, K_pri_Server = rsa.newkeys(keysz)

K_pub_pkda, K_pri_pkda = rsa.newkeys(keysz2)


AFile = open('A_keyInfo', 'wb+')
pickle.dump({"K_A_pri": K_pub_A}, AFile)

ServerFile = open('Server_keyInfo', 'wb+')
pickle.dump({"K_Server_pri": K_pub_Server}, ServerFile)



pkdaFile = open('pkda_keyInfo', 'wb+')

pickle.dump({"K_A_pub": K_pri_A, "K_Server_pub": K_pri_Server, "K_pkda_pri": K_pub_pkda}, pkdaFile)



BFile = open('B_keyInfo', 'wb+')

pickle.dump({"K_pkda_pub": K_pri_pkda}, BFile)



pkdaFile.close()
