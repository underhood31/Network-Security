from bitarray import bitarray
from bitarray import util

def get_column(arr, i):
    return [row[i] for row in arr]
def get_xor(arr):
    pass

class AES_Encryptor:
    def __init__(self):
        super().__init__()
        self.substitutionTable = None
        self.multiplyTable = None
        self.mixColTable = None
        self.key = None #rounds *4*4

    def to_state(self, inp):
        """
            converts 128 bit number to state representation
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
                state[rowNum, colNum] = self.substitutionTable[util.ba2int(inp[:4])][util.ba2int(inp[4:])]
        return state   

    
    def shiftRows(self, state):
        k = 1
        for i in range(1, 4):
            for _ in range(k):
                t = state[i][0]
                for j in range(3):
                    state[i][j] = state[i][j+1]
                state[i][3] = t
            k+=1
        return state

    def mixColumns(self, state):
        for i in range(4):
            col = get_column(state, i)
            
            for j in range(4):
                arr = []

                for k in range(4):
                    arr.append(self.multiplyTable[self.mixColTable[j][k]][col[k]])

                state[j][i] = get_xor(arr)
        return state

    def addRoundKey(self, state, roundNo):
        for i in range(4):
            for j in range(4):
                state[i][j] = state[i][j] ^ self.key[roundNo][i][j]

        return state

    def normalRound(self, state, roundNo):
        self.subBytes(state)
        self.shiftRows(state)
        self.mixColumns(state)
        self.addRoundKey(state, roundNo)
        

    def lastRound(self, state):
        self.subBytes(state)
        self.shiftRows(state)
        self.addRoundKey(state, 9)
        

    def encrypt(self , plaintext):
        state = self.to_state(plaintext)
        for i in range(9):
            self.normalRound(state, i)
        self.lastRound(state)
        encrypted = bitarray(128)
        for i in range(4):  #colNo
            for j in range(4):  #rowNo
                encrypted[32*i + 8*j : 32*i + 8*j + 8] = state[j][i]
        return encrypted

