import os

def bitxor(a, b):
    return "".join([str(int(x)^int(y)) for (x, y) in zip(a, b)])

def str2bin(ss):
    bs = ''
    for c in ss:
        bs = bs + bin(ord(c))[2:].zfill(8)
    return bs

def bin2hex(bs):
    return hex(int(bs,2))[2:-1]

class LFSR:
    def __init__(self, state, coeff):
        self.state = state
        self.coeff = coeff

    def tap(self):
        bits = [int(self.state[c-1]) for c in self.coeff]
        new_bit = reduce(lambda x,y:x^y, bits)

        result = self.state[-1]
        self.state = str(new_bit) + self.state[0:len(self.state)-1]
        return result

    def get_bits(self, nr_bits):
        bits = ""
        for _ in xrange(nr_bits):
            bits += self.tap()

        return bits

coeff = (88, 87, 17, 16)
state = str2bin(os.urandom(11))
prg = LFSR(state, coeff)

FLAG  = '-- redacted --'

bin_flag = str2bin(FLAG)
flag_enc = bin2hex(bitxor(bin_flag, prg.get_bits(len(bin_flag))))

print flag_enc