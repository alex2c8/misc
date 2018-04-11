"""
generate a 16384-bit RSA key
"""

from Crypto.PublicKey import RSA

# e is 65537 (default)
r = RSA.generate(16384)

f = open("sk.pem", "w")
f.write(r.exportKey('PEM'))
f.close()
print "DONE"
