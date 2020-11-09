import AES_Encryptor
import AES_Decryptor


if __name__=="__main__":
	cont=True
	while cont:
		name=input("Enter input file name: ")
		file=open(name,"r")
		key=file.readline()
		data=file.readline()
		print("1 --> Encrypt")
		print("2 --> Decrypt")
		print("3 --> Exit")
		i=input("Choice: ")
		if i=="1":
			enc=AES_Encryptor.AES_Encryptor(int(key,16))
			data_b=bin(int(data,16))[2:]
			st="For input data: "+data+"\nEncrypted data:"
			print(st,hex(int(enc.encrypt(data_b).to01(),2))[2:])

			c=input("Wanna continue?(Y/n) ")
			if c=="Y" or c=="y":
				continue
			else:
				break
		elif i=="2":
			enc=AES_Decryptor.AES_Decryptor(int(key,16))
			data_b=bin(int(data,16))[2:]
			st="For input data: "+data+"\nDecrypted data:"
			print(st,hex(int(enc.decrypt(data_b).to01(),2))[2:])

			c=input("Wanna continue?(Y/n) ")
			if c=="n":
				break
			else:
				continue
		elif i=="3":
			break
		else: 
			print("Wrong Choice. Try Again!!")
			continue
