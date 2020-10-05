import AES_Encryptor
import genRandKey
import numpy as np

def print_matrix(roundKey,i):
	mat=np.zeros([4,4],dtype='object')
	r=0
	for j in range(len(roundKey)):
		n=roundKey[j].to01()
		print(r+4*i,":",hex(int(n,2))[2:])
		r+=1
		# for i in range(0,32,8):
		# 	mat[j][i//8]=

	# print(mat)

if __name__=="__main__":
	# kg=genRandKey.GenerateRandomKey()
	# key=kg.generate(128)
	key=0x2b7e151628aed2a6abf7158809cf4f3c
	enc=AES_Encryptor.AES_Encryptor(key)
	for i in range(11):
		print_matrix(enc.getRoundkey(),i)

