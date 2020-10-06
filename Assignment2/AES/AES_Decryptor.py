from bitarray import bitarray
from bitarray import util
from pyfinite import ffield
import sys
import copy
# # Example code for finite fields
# a = 0xbf
# b = 0x03
# F = ffield.FField(8, gen=0b100011011, useLUT=0)  #Gen is the modulus term and useLookUpTables=false
# c = F.Multiply(a, b)
# print(hex(c))



def get_column(arr, i):
    return [util.ba2int(row[i]) for row in arr]
def get_xor(arr):
    ans  = arr[0]
    for i in range(1, len(arr)):
        ans  = ans ^ arr[i]
    return ans

def leftshift(bitarr, shifts):
    """
    The circular left shift for bitarray
    """
    return bitarr[shifts:] + (bitarr[0:shifts])

def rightshift(bitarr, shifts):
    """
    The circular right shift for bitarray
    """
    return bitarr[-shifts:] + (bitarr[0:-shifts])


class AES_Decryptor:
    def __init__(self, key, rounds=10):
        super().__init__()
        if(rounds==10):
            self.keySize=128
        elif(rounds==12):
            self.keySize=192
        elif(rounds==14):
            self.keySize=256
        else:
            raise Exception("Only 10, 12, 14 rounds allowed")
        self.key=self.to_state(self.convertToBitarray(key))
        self.roundKey=None
        self.rounds=rounds
        self.substitutionTable = None
        self.multiplyTable = None
        self.mixColTable = [[0x0e, 0x0b, 0x0d, 0x09], [0x09, 0x0e, 0x0b, 0x0d], [0x0d, 0x09, 0x0e, 0x0b], [0x0b, 0x0d, 0x09, 0x0e]]
        self.rc=0x01
        self.GF = ffield.FField(8, gen=0b100011011, useLUT=0)
        self.substitutionTable  =[[0x52,0x09,0x6a,0xd5,0x30,0x36,0xa5,0x38,0xbf,0x40,0xa3,0x9e,0x81,0xf3,0xd7,0xfb],
                                  [0x7c,0xe3,0x39,0x82,0x9b,0x2f,0xff,0x87,0x34,0x8e,0x43,0x44,0xc4,0xde,0xe9,0xcb],
                                  [0x54,0x7b,0x94,0x32,0xa6,0xc2,0x23,0x3d,0xee,0x4c,0x95,0x0b,0x42,0xfa,0xc3,0x4e],
                                  [0x08,0x2e,0xa1,0x66,0x28,0xd9,0x24,0xb2,0x76,0x5b,0xa2,0x49,0x6d,0x8b,0xd1,0x25],
                                  [0x72,0xf8,0xf6,0x64,0x86,0x68,0x98,0x16,0xd4,0xa4,0x5c,0xcc,0x5d,0x65,0xb6,0x92],
                                  [0x6c,0x70,0x48,0x50,0xfd,0xed,0xb9,0xda,0x5e,0x15,0x46,0x57,0xa7,0x8d,0x9d,0x84],
                                  [0x90,0xd8,0xab,0x00,0x8c,0xbc,0xd3,0x0a,0xf7,0xe4,0x58,0x05,0xb8,0xb3,0x45,0x06],
                                  [0xd0,0x2c,0x1e,0x8f,0xca,0x3f,0x0f,0x02,0xc1,0xaf,0xbd,0x03,0x01,0x13,0x8a,0x6b],
                                  [0x3a,0x91,0x11,0x41,0x4f,0x67,0xdc,0xea,0x97,0xf2,0xcf,0xce,0xf0,0xb4,0xe6,0x73],
                                  [0x96,0xac,0x74,0x22,0xe7,0xad,0x35,0x85,0xe2,0xf9,0x37,0xe8,0x1c,0x75,0xdf,0x6e],
                                  [0x47,0xf1,0x1a,0x71,0x1d,0x29,0xc5,0x89,0x6f,0xb7,0x62,0x0e,0xaa,0x18,0xbe,0x1b],
                                  [0xfc,0x56,0x3e,0x4b,0xc6,0xd2,0x79,0x20,0x9a,0xdb,0xc0,0xfe,0x78,0xcd,0x5a,0xf4],
                                  [0x1f,0xdd,0xa8,0x33,0x88,0x07,0xc7,0x31,0xb1,0x12,0x10,0x59,0x27,0x80,0xec,0x5f],
                                  [0x60,0x51,0x7f,0xa9,0x19,0xb5,0x4a,0x0d,0x2d,0xe5,0x7a,0x9f,0x93,0xc9,0x9c,0xef],
                                  [0xa0,0xe0,0x3b,0x4d,0xae,0x2a,0xf5,0xb0,0xc8,0xeb,0xbb,0x3c,0x83,0x53,0x99,0x61],
                                  [0x17,0x2b,0x04,0x7e,0xba,0x77,0xd6,0x26,0xe1,0x69,0x14,0x63,0x55,0x21,0x0c,0x7d]] # he prabhu  #phew...

    def convertToBitarray(self,key):
        """
            Converts given key into bitarray
        """
        inString=bin(key)[2:]
        rem=self.keySize-len(inString)
        inString="0"*rem+inString
        return bitarray(inString)

    def gfMultiply(self, a,b ):
        """
            Performs galwa field 2^8 multiplication
            a -> Integer
            b -> Integer
            Return type -> bitarray
        """
        F = ffield.FField(8, gen=0b100011011, useLUT=0)  #Gen is the modulus term and useLookUpTables=false
        c = F.Multiply(a, b)
        return util.int2ba( c, length=8, endian='big')
            

    def getRoundkey(self):
        """
            Returns the key to be used in the current round in form of [32bits, 32bits, 32bits, 32bits]

            ----------------------------------------------------TODO: ADD compatibility for 192 and 256 bit input-----------------------------------------
        """

        if(self.roundKey==None):
            self.roundKey=[]
            for i in range(len(self.key)):
                entry=bitarray()
                for j in range(len(self.key)):
                    entry=entry+self.key[j][i]
                self.roundKey.append(entry)
        else:
            g=copy.deepcopy(self.roundKey[-1])
            
            #left shift
            g=leftshift(g,8)

            #substitution
            new_g=bitarray()
            for i in range(0,32,8):
                num=int(g[i:i+8].to01(),2)
                num=hex(num)[2:]
                num='0'*(2-len(num))+num
                inString=(bin(self.substitutionTable[int(num[0],16)][int(num[1],16)])[2:])
                rem=8-len(inString)
                inString="0"*rem+inString
                new_g+=bitarray(inString)
            g=new_g

            rc_cur=bin(self.rc)[2:]
            rc_cur='0'*(8-len(rc_cur))+rc_cur
            rcbit=bitarray(rc_cur+'0'*24)
            self.rc=self.GF.Multiply(2,self.rc)

            #xoring rc and g
            g=g^rcbit

            #now generating key
            newRoundkey=[]

            newRoundkey.append(self.roundKey[0]^g)
            newRoundkey.append(self.roundKey[1]^newRoundkey[0])
            newRoundkey.append(self.roundKey[2]^newRoundkey[1])
            newRoundkey.append(self.roundKey[3]^newRoundkey[2])

            self.roundKey=newRoundkey
        return self.roundKey

    def to_state(self, inp):
        """
            converts 128 bit number to tate representation
            ---------------------------s-------------------------TODO: ADD compatibility for 192 and 256 bit input-----------------------------------------
        """
        state = []
        j = 0
        while(j<32):
            i = j
            s = []
            while(i<128):
                s.append(inp[i:i+8])
                i+=32
            state.append(s)
            j+=8
        return state


    def readKey(self):
        pass

    def subBytes(self, state):
        for rowNum, row in enumerate(state):
            for colNum, inp in enumerate(row):
                state[rowNum][colNum] = util.int2ba(self.substitutionTable[util.ba2int(inp[:4])][util.ba2int(inp[4:])], length=8, endian='big')
        return state   

    
    def shiftRows(self, state):
        k = 1
        for i in range(1, 4):
            for _ in range(k):
                t = state[i][3]
                for j in range(3,0,-1):
                    state[i][j] = state[i][j-1]
                state[i][0] = t
            k+=1
        return state

    def mixColumns(self, state):
        for i in range(4):
            col = get_column(state, i)
            
            for j in range(4):
                arr = []

                for k in range(4):
                    arr.append(self.gfMultiply(self.mixColTable[j][k], col[k]))

                state[j][i] = get_xor(arr)
        return state

    def convertKeyto4x4(self,key):
        toRet=[]
        for i in range(4):
            temp=[0]*4
            toRet.append(temp)

        for j in range(len(key)):
            num=key[j].to01()
            temp=[]
            for i in range(0,32,8):
                toRet[i//8][j]=bitarray(num[i:i+8])
        return toRet

    def addRoundKey(self, state):
        key=self.getRoundkey()
        key=self.convertKeyto4x4(key)

        for i in range(4):
            for j in range(4):
                state[i][j] = state[i][j] ^ key[i][j]
        return state

    def normalRound(self, state):
        self.subBytes(state)
        self.shiftRows(state)
        self.mixColumns(state)
        self.addRoundKey(state)
        

    def lastRound(self, state):
        self.subBytes(state)
        self.shiftRows(state)
        self.addRoundKey(state)
        

    def print_mat(self,state):
        for i in state:
            for j in i:
                print(hex(int(j.to01(),2)),end="\t")
            print()
        print()
    def decrypt(self , plaintext):
        #Plaintext as string of bits "011010101"
        #TODO: if len(plaintext)>128 do looping
        plaintext='0'*(128-len(plaintext))+plaintext
        plaintext=bitarray(plaintext)
        state = self.to_state(plaintext)

        self.addRoundKey(state)
        for i in range(9):
            self.normalRound(state)
        self.lastRound(state)
        decrypted = bitarray(128)
        for i in range(4):  #colNo
            for j in range(4):  #rowNo
                decrypted[32*i + 8*j : 32*i + 8*j + 8] = state[j][i]
        self.print_mat(state)
        return decrypted

