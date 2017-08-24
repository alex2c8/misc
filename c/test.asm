section     .text

global _start

_start:                                         ;tell linker entry point

    mov     eax,1                               ;system call number (sys_exit)
    int     0x80                                ;call kernel

section     .data

