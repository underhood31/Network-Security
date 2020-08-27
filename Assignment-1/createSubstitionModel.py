import copy
import random
import pickle
if __name__=="__main__":
	#creating a set to store all permutions
	allPerms=set()

	#calculating and saving all permutaions
	for i in range(97,97+26):
		for j in range(97,97+26):
			perm=chr(i)+chr(j)
			allPerms.add(perm)

	#converting the set to the list
	allPerms=list(allPerms)
	
	#creating another set of permutions and randomizing it
	allRandPerms=copy.deepcopy(allPerms)
	random.shuffle(allRandPerms)

	#exporting both the lists for use in encryption and decryption
	unshuf=open("unshuffuled.list","wb")
	pickle.dump(allPerms,unshuf)

	shuf=open("shuffled.list","wb")
	pickle.dump(allRandPerms,shuf);


