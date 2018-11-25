import gmpy2

def integer_to_bytes(integer):
    k = integer.bit_length()

    # adjust number of bytes
    bytes_length = k // 8 + (k % 8 > 0)

    bytes_obj = integer.to_bytes(bytes_length, byteorder='big')

    return bytes_obj


lines = [x.strip() for x in open("flipping_bits.txt").readlines()]

d = {}
for l in lines:
    k, v = l.split(":")
    d[k.strip()] = int(v.strip())
    if "modulus" in k:
        break


c1, c2 = d['ct1'], d['ct2']
modulus = d['modulus']
e1, e2 = d['e1'], d['e2']

y = (c2 * gmpy2.invert(c1, modulus)) % modulus
y = (y ** 6) % modulus
y = (c1 * gmpy2.invert(y, modulus)) % modulus

print(y)
m = integer_to_bytes(int(y))

print(m)
print("---")
