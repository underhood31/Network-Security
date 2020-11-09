import AES_Encryptor
import AES_Decryptor
import genRandKey
import numpy as np
from bitarray import bitarray

def print_mat(state):
        for i in state:
            for j in i:
                print(hex(int(j.to01(),2)),end="\t")
            print()
        print()

def convertKeyto4x4(key):
    toRet=[]
    for i in range(4):
        temp=[0]*4
        toRet.append(temp)

    for j in range(len(key)):
        num=key[j].to01()
        temp=[]
        for i in range(0,32,8):
            toRet[i//8][j]=bitarray(num[i:i+8])
    return toRet


def print_matrix(roundKey,i):
	print()
	print_mat(convertKeyto4x4(roundKey))
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
	#-----------For encryptor---------------
	# key=0x000102030405060708090a0b0c0d0e0f
	# enc=AES_Encryptor.AES_Encryptor(key)
	# for i in range(11):
	# 	print_matrix(enc.getRoundkey(),i)

	#-----------For decryptor---------------
	key=0x000102030405060708090a0b0c0d0e0f
	enc=AES_Decryptor.AES_Decryptor(key)
	for i in range(11):
		print_matrix(enc.getRoundkey(),i)
