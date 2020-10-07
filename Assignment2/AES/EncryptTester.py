import AES_Encryptor

key=0x2b7e151628aed2a6abf7158809cf4f3c
# key=0x000102030405060708090a0b0c0d0e0f
enc=AES_Encryptor.AES_Encryptor(key)
inp=bin(0x3243f6a8885a308d313198a2e0370734)[2:]
# inp=bin(0x00112233445566778899aabbccddeeff)[2:]
print(inp,len(inp))
print(hex(int(enc.encrypt(inp).to01(),2)))


