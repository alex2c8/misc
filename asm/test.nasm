section .text
    global _start

_start:
    mov eax, 0x08048540
    call eax
