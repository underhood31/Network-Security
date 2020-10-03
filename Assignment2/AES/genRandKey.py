import random

class GenerateRandomKey:
	def generate(size):
		key=random.getrandbits(size)
		print("Key is:",hex(key))
		return key