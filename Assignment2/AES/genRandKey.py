import random

class GenerateRandomKey:
	def generate(self,size):
		key=random.getrandbits(size)
		return key