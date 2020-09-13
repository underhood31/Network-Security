import copy
import random
import pickle
if __name__=="__main__":
	#creating a set to store all permutions
	# allPerms=set()

	# #calculating and saving all permutaions
	# for i in range(97,97+26):
	# 	for j in range(97,97+26):
	# 		perm=chr(i)+chr(j)
	# 		allPerms.add(perm)

	# #converting the set to the list
	# allPerms=list(allPerms)
	
	# #creating another set of permutions and randomizing it
	# allRandPerms=copy.deepcopy(allPerms)
    pairs = ['AA', 'AB', 'AC', 'BB', 'BA', 'BC', 'CC', 'CA', 'CB']

    indxDict  = {'AA':0, 'AB':1, 'AC':2, 'BB':3, 'BA':4, 'BC':5, 'CC':6, 'CA':7, 'CB':8}

    perm = copy.deepcopy(pairs)
	random.shuffle(perm)
    
	#exporting both the lists for use in encryption and decryption
	encrypt=open("encryption.list","wb")
	pickle.dump(perm, encrypt)
    
    reversePerm = ['AA']*9

    for i in range(9):
        reversePerm[indxDict[perm[i]]] = pairs[i]

	shuf=open("decryption.list","wb")
	pickle.dump(reversePerm,shuf);


