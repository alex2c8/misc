replace nops at the end of main with a call to call_me
instr = call <addr> such that it will call call_me
because of relative addressing, 
<addr> is = 0x100000000 + addr(call_me) - addr(next_instr_after(call call_me)) = 0xfffff59
therefore, 
40070b:	e8 59 ff ff ff       	call   400669 <call_me>

