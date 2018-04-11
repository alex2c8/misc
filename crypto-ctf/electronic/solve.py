"""
ECB Choosen Plaintext Attack

Bruteforce each char from each block. The flag is 44 bytes long,
so it uses 3 blocks => 3 rounds of bruteforce.

In the first round, we want to find the first 16 chars of the flag.
Start by sending a dummy block of 15 chars; this means that the last byte of the current block
will be the first char of the flag (since the blocksize = 16)

We ask the oracle to give the encryption of (15 * 'a' + flag[0]). This will be our
target ciphertext, we need to find a char that will match the corresponding encrypted char
for flag[0].

Now we send s1 = (15 * 'a' + guess) and we do this for each value of the char 'guess'.
When we find a value for guess s.t. when encrypting s1 we find the target ciphertext mentioned above,
this means that the first char of the flag is this guessed char (g0)

Next, we send s2 = (14 * 'a' + g0 + guess) and we repeat the procedure described above.
We will now find the second char of the flag (g0).

After finding the first block of the flag, we have to find the other 2.
Now, we know the previous block, so we won't send dummy 'a's anymore. Instead we will send
the previous block minus pad_len chars and we will append our guess and we will look
at the corresponding encrypted block.
"""

from pwn import *
import base64

flag_len = 44

r = remote("141.85.224.115", 12345)

prompt = "Enter plaintext (base64): "
out = "Ciphertext (hex) is: "

pad_byte = 'a'

def send(m):
    r.sendline(base64.b64encode(m))

def recv():
    return str(r.read()[len(out):][:-len(prompt)-1])


# we know that the flag uses 3 16b blocks
blocks = ["", "", ""]

# consume prompt
r.readuntil(prompt)

# bruteforce each byte from each block
for b in range(3):

    previous = 16 * pad_byte if b == 0 else blocks[b-1]

    # for each byte in block (blocksize = 16)
    for i in range(16):
        pad_len = len(blocks[b]) + 1
        prefix = previous[pad_len:]

        # first pad_len bytes from FLAG will also be encrypted in the first block
        send(prefix)
        ciphertext = recv()

        # previous + what i know so far = 15 bytes
        # last byte is bruteforced
        prefix += blocks[b]

        # make a guess for the correct char (try each ASCII)
        for c in range(128):
            guess = prefix + chr(c)

            send(guess)
            enc_guess = recv()

            # since oracle returns encrypt(plaintext + FLAG),
            # look at corresponding target ciphertext
            # 2 * 16 because 1 byte takes 2 hex chars
            if enc_guess[0:32] == ciphertext[b*32:b*32+32]:
                print i, chr(c)
                blocks[b] += chr(c)
                break


flag = blocks[0] + blocks[1] + blocks[2][:-4]
print flag
