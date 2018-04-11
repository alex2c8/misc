"""
For this task, I generated a 16384-bit RSA key (keygen.py) and saved it in sk.pem
The modulus n is sent to the server. It encrypts a random number (nonce), as
c = nonce ^ e (mod n), and then the server sends this c.
Therefore, I can decrypt it (find nonce), by running key.decrypt(c), where
key is the imported key (sk.pem).

To decrypt, d is needed. RSA generates this parameter as d = modular inverse
of e w.r.t. phi (phi = (p-1) * (q-1), where p * q = n).
"""

from pwn import *
from Crypto.PublicKey import RSA

key = RSA.importKey(open('sk.pem','r').read())
n = key.n
e = key.e

r = remote('141.85.224.115', 33333)
r.readuntil("65537.")

r.sendline(str(n))

x = r.readuntil("Give me the nonce")

o1 = len("Encrypted nonce is  ")
o2 = len("Give me the nonce ")

c = int(x[o1:][:-o2])

m = key.decrypt(c)
r.sendline(str(m))

r.interactive()
