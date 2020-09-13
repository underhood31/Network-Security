import pickle
import hashlib

indxDict  = {'AA':0, 'AB':1, 'AC':2, 'BB':3, 'BA':4, 'BC':5, 'CC':6, 'CA':7, 'CB':8}

class Encrypt:
	
	def __init__(self):
		self.load_substitution_table()
	
	def load_substitution_table(self):
		"""
		This function loads all permutions and randomized 
		permutations from external files, map them in a 
		dictionary and return the dictionary
		"""
		# unshuf=open("unshuffuled.list","wb")
		# allPerms=pickle.load(unshuf)

		# shuf=open("shuffled.list","wb")
		# allRandPerms=pickle.dump(shuf)
        shuf=open("encryption.list","wb")
		self.substitution_table =pickle.load(shuf)

		# for i in range(len(allPerms)):
		# 	tablle[allPerms[i]]=allRandPerms[i]

		# self.substitution_table=table

	def encrypt(self, plaintext):
		"""
		Return the encrypted plain text
		"""

		#TODO: Handle the case if plaintext is odd in length
        if (len(plaintext)%2==1):
            plaintext+='C'

		cipher=''
		for i in range(0,len(plaintext),2):
			try:
				inp=plaintext[i]+plaintext[i+1]
				cipher+=self.substitution_table[indxDict[inp]]
                
			except:
				print("Error occured")
        cipher += hashlib.md5(plaintext.encode('utf-8')).hexdigest()
		return cipher
