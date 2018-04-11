#!/usr/bin/python -u
import os
import sys
import time
from Crypto.Util import number
from random import randint

e = 65537
timeout = 5
flag = '-- redacted --'

print "Generate your RSA key and give me your 'N'."
print "It should have at least 16384 bits."
print "Note that your 'e' should be 65537."

n = int(raw_input())
nr_bits = len(bin(n)[2:])

if nr_bits < 16384:
    print 'Your N has %s bits, less than 16384 bits.' % nr_bits
    exit(1)
else:
    nonce = randint(2, n-1)
    # c = (nonce ** e) % n
    c = pow(nonce, e, n)
    print 'Encrypted nonce is ' + str(c)
    print 'Give me the nonce'

    begin = time.time()
    iput = raw_input()
    end = time.time()
    print 'it took you %s seconds to decrypt, timeout is %s seconds' % ((end-begin), timeout)

    if end-begin > timeout:
        print "try harder"
    elif int(iput) == nonce:
        print flag
    else:
        print "incorrect nonce"

