import pickle

class encrypt:
	
	def __init__(self):
		self.load_substitution_table()
	
	def load_substitution_table(self):
		"""
		This function loads all permutions and randomized 
		permutations from external files, map them in a 
		dictionary and return the dictionary
		"""
		unshuf=open("unshuffuled.list","wb")
		allPerms=pickle.load(unshuf)

		shuf=open("shuffled.list","wb")
		allRandPerms=pickle.dump(shuf);

		table={}

		for i in range(len(allPerms)):
			tablle[allPerms[i]]=allRandPerms[i]

		self.substitution_table=table

	def encrypt(self.plaintext):
		"""
		Return the encrypted plain text
		"""

		#TODO: Handle the case if plaintext is odd in length

		cipher=''
		for i in range(0,len(plaintext),2):
			try:
				inp=plaintext[i]+plaintext[i+1]
				cipher+=self.substitution_table[inp]
			except:
				cipher+=plaintext[i]

		return cipher
