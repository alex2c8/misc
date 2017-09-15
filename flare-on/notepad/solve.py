hex1 = "558BEC8B4D0C5657"
hex2 = "8B550852FF153020"
hex3 = "C04050FFD683C408"
hex4 = "0083C4085DC3CCCC"

KEY = "".join([hex1, hex2, hex3, hex4])
bKEY = bytearray.fromhex(KEY)
KEY_SIZE = len(bKEY)

WEIRD = "37E7D8BE7A533025BB38572697266F50F47567BFB0EFA57A65AEAB6673A0A3A1"
bWEIRD = bytearray.fromhex(WEIRD)
WEIRD_SIZE = len(bWEIRD)

FLAG = [''] * WEIRD_SIZE

def XOR():
   for i in range(0, WEIRD_SIZE):
       FLAG[i] = bWEIRD[i] ^ bKEY[i % KEY_SIZE]

if __name__ == '__main__':
    XOR()
    print "".join(map(lambda x : chr(x), FLAG))