import curses
from encrypt import *
from decrypt import *
from bruteforce import *
import model as csm
encrypt=None
decrypt=None
bruteforce=None

def main(window):
	curses.curs_set(0)
	curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE) #Selected
	curses.init_pair(2,curses.COLOR_WHITE,curses.COLOR_BLACK) #DeSelected
	
	window.attron(curses.color_pair(2))
	h,w=window.getmaxyx()
	col=1
	curScreen=-1
	homeChoice=0
	encString=''
	encOut=''
	charChoice=0
	decStr=''
	decOut=''
	enkey=''
	brutarr=[]
	dic  = {'AA':0, 'AB':1, 'AC':2, 'BB':3, 'BA':4, 'BC':5, 'CC':6, 'CA':7, 'CB':8}

	while True:
		window.clear()
		string="Network Security Assignment 1"
		window.addstr(1,w//2-len(string)//2,string,curses.A_UNDERLINE)
		if curScreen==-1:
			header="Home"
			window.addstr(3,w//2-len(header)//2,header,curses.A_BOLD)
			if homeChoice==0:
				window.attron(curses.color_pair(1))
				window.addstr(6,w//2-len("Encrypt")//2,"Encrypt")
				window.attron(curses.color_pair(2))
			else:
				window.addstr(6,w//2-len("Encrypt")//2,"Encrypt")

			if homeChoice==1:
				window.attron(curses.color_pair(1))
				window.addstr(8,w//2-len("Decrypt")//2,"Decrypt")
				window.attron(curses.color_pair(2))
			else:
				window.addstr(8,w//2-len("Decrypt")//2,"Decrypt")

			if homeChoice==2:
				window.attron(curses.color_pair(1))
				window.addstr(10,w//2-len("Bruteforce, load from ./ciphers.txt")//2,"Bruteforce, load from ./ciphers.txt")
				window.attron(curses.color_pair(2))
			else:
				window.addstr(10,w//2-len("Bruteforce, load from ./ciphers.txt")//2,"Bruteforce, load from ./ciphers.txt")
		elif curScreen==0:
			header="Encrypt"
			window.addstr(3,w//2-len(header)//2,header,curses.A_BOLD)
			window.attron(curses.color_pair(1))
			window.addstr(6,w//2-len(encString)//2,encString,curses.A_BLINK)
			window.attron(curses.color_pair(2))

			message="Input Characters(press D when done, and TAB to go back):"
			window.addstr(8,w//2-len(message)//2,message,curses.A_DIM)

			if charChoice==0:
				window.attron(curses.color_pair(1))
				window.addstr(10,w//2-8,"A")
				window.attron(curses.color_pair(2))
			else:
				window.addstr(10,w//2-8,"A")

			if charChoice==1:
				window.attron(curses.color_pair(1))
				window.addstr(10,w//2-4,"B")
				window.attron(curses.color_pair(2))
			else:
				window.addstr(10,w//2-4,"B")

			if charChoice==2:
				window.attron(curses.color_pair(1))
				window.addstr(10,w//2,"C")
				window.attron(curses.color_pair(2))
			else:
				window.addstr(10,w//2,"C")
			if charChoice==3:
				window.attron(curses.color_pair(1))
				window.addstr(10,w//2+4,"DEL")
				window.attron(curses.color_pair(2))
			else:
				window.addstr(10,w//2+4,"DEL")

			if(encOut!=''):
				out="Encrypted string is: "+encOut
				window.addstr(13,w//2-len(out)//2,out)
				window.addstr(14,w//2-len(str(dic))//2,str(dic))
				window.addstr(15,w//2-len(enkey)//2,enkey)

		elif curScreen==1:
			header="Decrypt"
			window.addstr(3,w//2-len(header)//2,header,curses.A_BOLD)
			out="Enter cyphertext to decrypt(Press TAB to go back): "
			window.addstr(5,w//2-len(out)//2,out)
			
			window.attron(curses.color_pair(1))
			window.addstr(6,w//2-len(decStr)//2,decStr)
			window.attron(curses.color_pair(2))

			if(decOut!=''):
				out="Decrepted string is: "+decOut
				window.addstr(13,w//2-len(out)//2,out)
				window.addstr(14,w//2-len(str(dic))//2,str(dic))
				window.addstr(15,w//2-len(enkey)//2,enkey)
			
		elif curScreen==2:
			header="Bruteforce, , loaded from ./ciphers.txt"
			window.addstr(3,w//2-len(header)//2,header,curses.A_BOLD)
			out="Press TAB to go back "
			window.addstr(5,w//2-len(out)//2,out)
			
			window.attron(curses.color_pair(1))
			window.addstr(7,w//2-len("> Load")//2,"> Load")
			window.attron(curses.color_pair(2))

			

			if(len(brutarr)>0):
				for i in range(len(brutarr)):
					window.addstr(9+i,w//2-(len(brutarr[i]))//2,brutarr[i])

				out="Plain text is: "+decOut
				window.addstr(13,w//2-len(out)//2,out)
				window.addstr(14,w//2-len(str(dic))//2,str(dic))
				window.addstr(15,w//2-len(enkey)//2,enkey)
			


		inp=window.getch()
		# if(inp==curses.KEY_LEFT or inp==curses.KEY_RIGHT):

		#     col+=1
		if  inp==27:
			break
		elif curScreen==-1:
			if inp==curses.KEY_UP:
				homeChoice=(homeChoice-1)%3
			elif inp==curses.KEY_DOWN:
				homeChoice=(homeChoice+1)%3
			elif inp==curses.KEY_RIGHT or inp==curses.KEY_ENTER or inp==13 or inp==10:
				curScreen=homeChoice
				homeChoice=0
		elif curScreen==0:
			if inp==curses.KEY_LEFT:
				charChoice=(charChoice-1)%4
			elif inp==curses.KEY_RIGHT:
				charChoice=(charChoice+1)%4
			elif inp==curses.KEY_ENTER or inp==13 or inp==10\
				 and charChoice==0:
				encString+='A'
			elif inp==curses.KEY_ENTER or inp==13 or inp==10\
				 and charChoice==1:
				encString+='B'
			elif inp==curses.KEY_ENTER or inp==13 or inp==10\
				 and charChoice==2:
				encString+='C'
			elif inp==curses.KEY_ENTER or inp==13 or inp==10\
				 and charChoice==3:
				encString=encString[:len(encString)-1]
			elif inp==68 or inp==100:
				encOut,enkey=encrypt.encrypt(encString)
			elif inp==9:
				charChoice=0
				encString=''
				encOut=''
				curScreen=-1
		elif curScreen==1:
			if inp==9:
				decStr=''
				curScreen=-1
				decOut=''
			elif chr(inp).isalnum() and inp < 96+26:
				decStr+=chr(inp)
			elif inp==263:#backspace
				decStr=decStr[:len(decStr)-1]
			elif inp==curses.KEY_ENTER or inp==13 or inp==10:
				decOut,hashs,enkey=decrypt.decrypt(decStr)
		elif curScreen==2:
			if inp==9:
				decStr=''
				curScreen=-1
				decOut=''
			# elif chr(inp).isalnum() and inp < 96+26:
			# 	decStr+=chr(inp)
			# elif inp==263:#backspace
			# 	decStr=decStr[:len(decStr)-1]
			elif inp==curses.KEY_ENTER or inp==13 or inp==10:
				brutarr,enkey=bruteforce.bruteforce()

if __name__=="__main__":
	# print("1. Encrypt")
	# print("2. Decrypt")
	# print("3. Bruteforce")
	# val=int(input(":"))

	# while True:
	# 	if val==1:
	# 		pass
	# 	elif val==2:
	# 		pass	
	# 	elif val==3:
	# 		pass
	# print("ff")
	# enc=encrypt.encrypt("ABAC")
	# print(enc)
	# print(decrypt.decrypt("CCBCabdc72442c6c3a7927a42ccd38932a24"))
	# print(bruteforce.bruteforce(enc))
	# csm.main()
	encrypt=Encrypt()
	decrypt=Decrypt()
	bruteforce=Bruteforce()
	# a,b=bruteforce.bruteforce()
	# print(a,b)
	# enc=encrypt.encrypt("ABAC")
	# print(enc)
	# print(decrypt.decrypt(enc[0]))
	curses.wrapper(main)

		
