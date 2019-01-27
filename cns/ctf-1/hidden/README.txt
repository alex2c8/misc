discover a function f with 4 params (not initially visible to ida)
set params such that decrypt flag will be called
use gdb to set the params accordingly
p1:   set $rdi=0x4e43
p2:   set $rsi=0x4353 
p3:   set $rdx=0x4654 
p4:   set $rcx=0x601144
jump: set $rip=0x400599 (addr of f)
