import random

class GenerateRandomKey:
	def generate(self,size):
		key=random.getrandbits(size)
		print(hex(key)[2:])
		return key

if __name__ == "__main__":
    GenerateRandomKey().generate(128)