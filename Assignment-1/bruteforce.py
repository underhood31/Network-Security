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

	def bruteforce(self,ciphertext):
		brutecrypt=''
		allPerm = list(permutations(pairs))
		correctKey=''
		validKey=False
		for key in allPerm:
			Decrypter = Decrypt(key)
			brutecrypt,hashs=Decrypter.decrypt(ciphertext)
			# print("::",brutecrypt,hashs)
			validKey = self.validDecode(brutecrypt, hashs)
			if (validKey):
				correctKey=key
				break
		if not validKey:
			return "Invalid cyphertext"
		# print("Key: ", key,"\nPlaintext: ",brutecrypt)
		return brutecrypt

