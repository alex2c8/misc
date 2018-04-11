"""
Because the RSA keys were generated on the same computer, there is a high chance
that the modulos used (n) share a common prime (i.e. gcd(n_alice, n_bob) != 1,
gcd(n_alice, n_bob) = common_prime).
Using this common prime, we can find the other prime, as well as phi and d,
for both Alice and Bob.
We know that d = modular inverse of e w.r.t phi
Having d_alice and d_bob we can decrypt their messages, concatenate them and
find the flag.
"""

from Crypto.PublicKey import RSA
import base64
from gmpy2 import gcd

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a,a)
    return (g, x - (b//a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x%m

c_alice_b64 = open('for_alice.enc', 'rt').readline().strip()
c_bob_b64 = open('for_bob.enc', 'rt').readline().strip()

c_alice = base64.b64decode(c_alice_b64)
c_bob = base64.b64decode(c_bob_b64)

# n -> 2048 bits
# both
e = 65537L
pk_alice = RSA.importKey(open("alice.pubkey").read())
pk_bob = RSA.importKey(open('bob.pubkey').read())

# their n share a common prime
common_prime = long(gcd(pk_alice.n, pk_bob.n))

# n_alice = p1 * common_prime
p1 = long(pk_alice.n / common_prime)
# n_bob = p2 * common_prime
p2 = long(pk_bob.n / common_prime)

phi_alice = (p1 - 1) * (common_prime - 1)
d_alice = modinv(e, phi_alice)
alice = RSA.construct((pk_alice.n, e, d_alice))

phi_bob = (p2 - 1) * (common_prime - 1)
d_bob = modinv(e, phi_bob)
bob = RSA.construct((pk_bob.n, e, d_bob))

m_alice = alice.decrypt(c_alice)
m_bob = bob.decrypt(c_bob)

print "FLAG:", str(m_alice) + str(m_bob)

"""
ca = (ma ** e) % na
cb = (mb ** e) % nb

ma = (ca ** da) % na
mb = (cb ** db) % nb

na = pa * qa
nb = pb * qb

phia = (pa-1)*(qa-1)
phib = (pb-1)*(qb-1)

da*e = 1 (mod phia)
db*e = 1 (mod phib)
"""
