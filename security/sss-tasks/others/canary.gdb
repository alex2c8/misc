set disassembly-flavor intel
file gccStackPro
break *0x804844a
commands
p/x $eax
c
end
run
quit
