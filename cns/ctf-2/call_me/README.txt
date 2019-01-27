use gdb
find call_me address
set RIP = call_me address right before calling validate_hash (so that the argument is the same)
let call_me do its magic and get the flag from the stack
