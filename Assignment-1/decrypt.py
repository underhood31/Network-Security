import pickle


indxDict  = {'AA':0, 'AB':1, 'AC':2, 'BB':3, 'BA':4, 'BC':5, 'CC':6, 'CA':7, 'CB':8}

class Decrypt:
	
	def __init__(self, key = None):
		if (key == None):
			self.key = self.load_substitution_table()  

		else:
			self.key = key


	def load_substitution_table(self):
		"""
		This function loads all permutions and randomized 
		permutations from external files, map them in a 
		dictionary and return the dictionary
		# """
		# print("READ")
		shuf=open("decryption.list","rb")
		self.substitution_table =pickle.load(shuf)
		return self.substitution_table

	def decrypt(self, ciphertext):
		"""
		Return the encrypted plain text
		"""

		#TODO: Handle the case if plaintext is odd in length

		plaintxt=''
		# print("::",ciphertext)
		txt = ciphertext[:-32]
		# print("::",txt)
		for i in range(0,len(txt),2):
			# try:
			inp= txt[i]+ txt[i+1]
			plaintxt+=self.key[indxDict[inp]]
			
		return plaintxt,ciphertext[-32:],str(self.key)
