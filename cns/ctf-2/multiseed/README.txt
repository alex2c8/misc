we notice that each thread XORs the input given in argv[1]
with its series of rand values determined from its seed

let str = input for current thread
str[i] ^= rand, where rand is the current generated random value from thread's seed

each thread returns success iff str is the same as flag_enc

therefore, because seeds are _static_, we can compute
all random values that will be generated for each thread

next, for thread t to return success, it must be given as
input[i] = flag_enc[i] ^ rand[i]

thus, we extract the seeds and the encoded flag,
we compute the series of random values for each thread and the expected input

the flag must be among the constructed inputs;
we notice that input 5 gives us the flag (i.e. flag_enc ^ thread_5_rand_values == flag)
