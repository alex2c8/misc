import random
from math import floor

def encode(s):
    a = []
    for i in range(len(s)):
        t = ord(s[i])

        for j in range(8):
            if ((t >> j) & 1):
                a += [1 + j + (len(s) - 1 - i) * 8]

    print(a)

    """
    b = []
    while(len(a) > 0):
        t = floor(random.random() * len(a))
        b += [a[t]]
        a = a[:t] + a[t+1:]
    """
    b = a[:]
    random.shuffle(b)
    print(b)

    r = ""
    while len(b) > 0:
        t = b.pop()
        r += "-"*t + "."

    return r


def bits_to_char(bits):
    c = 0

    for b in bits:
        c += (1 << (b-1))

    return chr(c)

f = open("instructions.txt").readlines()[0].strip()

q = f.split(".")[:-1]
lmod = list(map(lambda a : len(a)%8, q))
ldiv = list(map(lambda a : len(a)//8, q))
z = list(zip(lmod, ldiv))


from operator import itemgetter
zs = sorted(z, key=itemgetter(1))

c = 0
s = []
out = []
i = 0
while i < len(zs):
    imod, idiv = zs[i]
    if idiv == c:
        s += [imod]
    else:
        c = idiv
        out += [s]
        s = [imod]
    i += 1
out += [s]


flag = "".join(list(map(bits_to_char, out))[::-1])
print(flag)
