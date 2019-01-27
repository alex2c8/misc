same as call_me_reloaded
patched 3 4bytes instructions after last close() call in main with

0x10728:	e3010337 	movw	r0, #4919	; 0x1337
0x1072c:	e28f1014 	add	r1, pc, #20
0x10730:	ebffffb3 	bl	10604 <call_me>
...
0x10748:	5f534e43 	.word	0x5f534e43 ; (CNS_)


first param:   r0 <- 0x1337
sencond param: r1 <- addr(0x5f534e43) = 0x10748 = (pc + 8) + 20 = 0x1072c + 28 = 0x10748
branch with link (call) call_me => call_me(0x1337, 0x10748)

call_me wants its first param = 0x1337,
and the first 3 bytes (little-endian) of the value at the address given
as its second param to be C, N, S
if so, it proceeds to decrypt the flag
