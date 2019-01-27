patch with call_me rel addr
patch edi = 0x1337 (first param)
patch esi = find CNS in gdb (second param)

call_me checks param1 == 0x1337 and first 3 bytes of value at param2 to be C, N, S

