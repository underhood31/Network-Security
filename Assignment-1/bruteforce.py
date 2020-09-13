from decrypt import Decrypt
from itertools import permutations
import hashlib

pairs = ['AA', 'AB', 'AC', 'BB', 'BA', 'BC', 'CC', 'CA', 'CB']

class bruteforce:
	
	def __init__(self):
		print("Input the cipher-strings for bruteforce")
        print("Enter 0 if you want to input from file and 1 if you want to input from console")
        self.ciphers = takeFromConsole()
		


	def takeFromConsole(self):
		n = input("Enter number of ciphertexts: ")
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
				validKey = validKey and validDecode(cipher[:-32], cipher[-32:])
				if (not validKey):
					break
			print("Valid Key found! Key: ", key)


