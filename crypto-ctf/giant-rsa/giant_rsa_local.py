#!/usr/bin/python -u
import os
import sys
import time
from Crypto.Util import number
from random import randint
import numpy as np
from Crypto.PublicKey import RSA


key = RSA.importKey(open('sk.pem','r').read())
n = key.n
e = key.e

timeout = 5
flag = '-- redacted --'

print "Generate your RSA key and give me your 'N'."
print "It should have at least 16384 bits."
print "Note that your 'e' should be 65537."

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
    m = key.decrypt(c)
    iput = m
    end = time.time()
    print 'it took you %s seconds to decrypt, timeout is %s seconds' % ((end-begin), timeout)

    ##if end-begin > timeout:
    # #   print "try harder"
    if int(iput) == nonce:
        print flag
    else:
        print "incorrect nonce"

