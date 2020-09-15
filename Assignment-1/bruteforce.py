from decrypt import Decrypt
from itertools import permutations
import hashlib

pairs = ['AA', 'AB', 'AC', 'BB', 'BA', 'BC', 'CC', 'CA', 'CB']

class Bruteforce:
	
	def __init__(self):
		# print("Input the cipher-strings for bruteforce")
		# print("Enter 0 if you want to input from file and 1 if you want to input from console")
		# self.ciphers = takeFromConsole()
		pass


	def takeFromConsole(self,n):
		lst = []
		try:
			n = int(n)
		except:
			print("Invalid input")
		for i in range(n):
			lst.append(input("Enter the cipherText: "))

		return lst

	def takeFromFile(self):
		
		return []

	def validDecode(self, plain, hashtxt):
		return (hashlib.md5(plain.encode('utf-8')).hexdigest() == hashtxt or (len(plain)>0 and hashlib.md5(plain[:-1].encode('utf-8')).hexdigest() == hashtxt) )


	def tryAllCombos(self):
		allPerm = list(permutations(pairs))
		for key in allPerm:
			Decrypter = Decrypt(key)
			validKey = True
			for cipher in self.ciphers:
				brutecrypt=Decrypter.decrypt(cipher)
				validKey = validKey and validDecode(brutecrypt[:-32], brutecrypt[-32:])
				if (not validKey):
					break
			print("Valid Key found! Key: ", key)

	def bruteforce(self):
		ciphers=[]
		# try:
		f = open("ciphers.txt", "r")
		ciphers.append(f.readline()[:-1])
		ciphers.append(f.readline()[:-1])
		ciphers.append(f.readline()[:-1])
		ciphers.append(f.readline())
		if ciphers[-1][-1]=='\n':
			ciphers[-1]=ciphers[-1][:-1]
			pass
		# except:
		# 	return [],""

		brutecrypt=''
		allPerm = list(permutations(pairs))
		correctKey=''
		validKey=False
		validarr=[]
		for key in allPerm:
			Decrypter = Decrypt(key)
			brutecrypt,hashs,keyy=Decrypter.decrypt(ciphers[0])
			# print("::",brutecrypt,hashs)
			validKey = self.validDecode(brutecrypt, hashs)
			if (not validKey):
				continue
			else:
				#test cipher 2
				c2,hashs2,keyy1=Decrypter.decrypt(ciphers[1])
				c3,hashs3,keyy2=Decrypter.decrypt(ciphers[2])
				c4,hashs4,keyy3=Decrypter.decrypt(ciphers[3])
				if(self.validDecode(c2,hashs2) and self.validDecode(c3,hashs3) and self.validDecode(c4,hashs4)):
					correctKey=key
					validarr.append(brutecrypt)
					validarr.append(c2)
					validarr.append(c3)
					validarr.append(c4)
					break
				else:
					validKey=False


		if not validKey:
			return [],"Not found"
		# print("Key: ", key,"\nPlaintext: ",brutecrypt)
		return validarr,str(correctKey)

