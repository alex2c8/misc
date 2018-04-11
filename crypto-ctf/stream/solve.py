"""
Upon closer inspection, we can determine the entire bitstream just by having the
initial state. We are interested in the birst 88 bits from the bitstream, that
will get xored with the first 88 bits from the flag ("CRYPTO_CTF{").
We find that after 88 taps, the first 88 bits from the bitstream are the reverse
of the initial state.
We know how the flag is supposed to look like, so:

bitstream[0:88] = reverse(initial_state)
flag_enc[0:88] = flag[0:88] XOR bitstream[0:88]
bitstream[0:88] = flag_enc[0:88] XOR "CRYPTO_CTF{"

This means that we cand find the initial state:
initial_state = reverse(flag_enc[0:88] XOR "CRYPTO_CTF{")

we than set the initial state for the LFSR to the one we found above and
get the bitstream by tapping the LFSR 352 number of times (352 = 8 * 44, 44 = length of the flag)

Then, the flag is just flag_enc XOR bitstream.
"""

import os
from utils import *
import binascii

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

def hex2ascii(l):
    f = lambda c : hex(ord(c))[2:].zfill(2)
    return "".join(list(map(f, l)))

coeff = (88, 87, 17, 16)

flag_enc = open("flag.enc", "rt").readline().strip()
bin_flag_enc = hex2bin(flag_enc)

S0 = bitxor(bin_flag_enc[0:88], str2bin("CRYPTO_CTF{"))
S0 = S0[::-1]

prg = LFSR(S0, coeff)
G = prg.get_bits(len(bin_flag_enc))

flag_dec = bin2hex(bitxor(bin_flag_enc, G))

print binascii.unhexlify(flag_dec)
