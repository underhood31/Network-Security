import AES_Decryptor

# key=0x000102030405060708090a0b0c0d0e0f
key=0x2b7e151628aed2a6abf7158809cf4f3c
enc=enc=AES_Decryptor.AES_Decryptor(key)
inp=bin(0x3925841d02dc09fbdc118597196a0b32)[2:]
# inp=bin(0x69c4e0d86a7b0430d8cdb78070b4c55a)[2:]
print(inp,len(inp))
print(hex(int(enc.decrypt(inp).to01(),2)))


