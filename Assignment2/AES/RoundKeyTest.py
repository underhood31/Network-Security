import AES_Encryptor
import genRandKey
import numpy as np


def print_matrix(roundKey):
	mat=np.zeros([4,4],dtype='object')

	for j in range(len(roundKey)):
		n=roundKey[j].to01()
		for i in range(0,32,8):
			mat[j][i//8]=hex(int(n[i:i+8],2))

	print(mat)

if __name__=="__main__":
	# kg=genRandKey.GenerateRandomKey()
	# key=kg.generate(128)
	key=0x2b7e151628aed2a6abf7158809cf4f3c
	enc=AES_Encryptor.AES_Encryptor(key)
	print_matrix(enc.getRoundkey())
	print_matrix(enc.getRoundkey())
