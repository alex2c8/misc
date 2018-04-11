"""
From pcap we get B = 150608872816.
Use pcap data to find Alice's secret key (a). Because the numbers are small, a bruteforce is feasible.
Now that we have a (= 712325), we can compute the key that was used in the conversation, as KEY = sha256(pow(B, a, p))
We decrypt the password and get "Th1sIsMySup3rSecur3P455w0rd".

Now we need to talk to the server. Generate B = pow(g, b, p), where b is rand([1, p-1]) and send it.
KEY = sha256(pow(B, a, p)) = sha256(pow(A, b, p)).

Now we send the password encrypted as [IV|AES-CBC(KEY, IV, password)]
At this point we can send encrypted commands. We want the flag, so we send the encryption of "cat /home/ctf2/flag".
We then get the encryption of the flag. We decrypt it with the KEY above.
"""


from pwn import *
import random
import binascii
from Crypto import Random
from hashlib import sha256
from Crypto.Cipher import AES


BLOCK_SIZE = 16

def pad(m):
    o = BLOCK_SIZE - len(m) % BLOCK_SIZE
    return m + o * chr(o)

def unpad(p):
    return p[0:-ord(p[-1])]

def encrypt(KEY, m):
    IV = R.read(BLOCK_SIZE)
    aes = AES.new(KEY, AES.MODE_CBC, IV)
    c = aes.encrypt(pad(m))
    return (IV + c).encode('hex')

def decrypt(KEY, c):
    data = c.strip().decode('hex')
    IV, data = data[:BLOCK_SIZE], data[BLOCK_SIZE:]
    aes = AES.new(KEY, AES.MODE_CBC, IV)
    #print aes.decrypt(data)
    m = unpad(aes.decrypt(data))
    return m



local = False

if not local:
    R = Random.new()

    r = remote("141.85.224.115", 54321)

    prompt = "Please supply B: "

    r.readuntil("p = ")
    p = long(r.readuntil("g = ")[:-len("g = ")-1])
    g = long(r.readuntil("A = ")[:-len("A = ")-1])
    A = long(r.readuntil(prompt)[:-len(prompt)-1])

    b = random.randint(1, p-1)
    B = pow(g, b, p)

    # K = B ^ a (mod p) = A ^ b (mod p)
    K = pow(A, b, p)
    KEY = sha256(str(K)).digest()

    # password, from local
    password = "Th1sIsMySup3rSecur3P455w0rd"

    print "p[" + str(p) + "]"
    print "g[" + str(g) + "]"
    print "A[" + str(A) + "]"
    print "B[" + str(B) + "]"
    print "K[" + str(KEY).encode("hex") + "]"

    r.sendline(str(B))

    pw_enc = encrypt(KEY, password)
    r.sendline(str(pw_enc))

    # cmd
    cmd = "cat /home/ctf2/flag"
    cmd_enc = encrypt(KEY, cmd)
    r.sendline(str(cmd_enc))

    # get encrypted flag
    flag_enc = str(r.read())
    flag = decrypt(KEY, flag_enc)

    print flag

else:
    # pcap data
    p = 751672198763
    g = 70600674451
    A = 518295907282
    B = 150608872816

    # from bruteforce.py
    a = 712325

    K = sha256(str(pow(B, a, p))).digest()

    pw_iv = "1b432628adcb5472f5a0e942a8e45578"
    pw_data = "d8908a278e1b704ec6ef6c74d03fde4d69f0a2c4206813b12acd49d7be467db5"

    password = decrypt(K, str(pw_iv + pw_data))
    print password

    iv = "14495841a3b7af157fda4d5bca62e010"
    data = "e788ac0369ba83f49e40dd9b9d6dda3f65975d43977c0cbb1da773791cd5404f97110e6b082e4ebd4931b6b41070de6b"

    m = decrypt(K, str(iv + data))
    print m

    iv = "efb9eae7dd4b69ef90de8b029748c744"
    data = "9a1defcd91c0c7ce4d303266b33a58303d5e7af22b8a1195bd83a89d7f3ef918"

    m = decrypt(K, str(iv + data))
    print m

"""
pcap:
Parameters:
p = 751672198763
g = 70600674451
A = 518295907282
Please supply B: 150608872816

some key K = sha256(pow(A, b, p)) = sha256(pow(B, a, p))

password (IV | data)                    = 1b432628adcb5472f5a0e942a8e45578 | d8908a278e1b704ec6ef6c74d03fde4d69f0a2c4206813b12acd49d7be467db5
cmd      (IV | cmd)                     = 14495841a3b7af157fda4d5bca62e010 | e788ac0369ba83f49e40dd9b9d6dda3f65975d43977c0cbb1da773791cd5404f97110e6b082e4ebd4931b6b41070de6b
flag     (IV | data)                    = efb9eae7dd4b69ef90de8b029748c744 | 9a1defcd91c0c7ce4d303266b33a58303d5e7af22b8a1195bd83a89d7f3ef918
"""
