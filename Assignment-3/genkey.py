import pickle

import rsa

keysz = 2048

k_pub_pkda , k_pri_pkda = rsa.newkeys(keysz)

k_pub_a, k_pri_a = rsa.newkeys(1024)

k_pub_b , k_pri_b = rsa.newkeys(1024)


pkdaFile = open('pkda_keyInfo', 'wb+')

pickle.dump({"k_pri_pkda": k_pub_pkda, "k_pub_a": k_pub_a, "k_pub_b": k_pub_b}, pkdaFile)

pkdaFile.close()

aFile = open('a_keyInfo', 'wb+')

pickle.dump({"k_pub_pkda": k_pri_pkda, "k_pri_a": k_pri_a}, aFile)

aFile.close()

bFile = open('b_keyInfo', 'wb+')

pickle.dump({"k_pub_pkda": k_pri_pkda, "k_pri_b": k_pri_b}, bFile)

bFile.close()