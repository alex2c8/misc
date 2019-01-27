# https://en.wikipedia.org/wiki/RC4#Key-scheduling_algorithm_(KSA)

def encode(key, length):
    out = [i for i in range(256)]

    acc = 0

    for j in range(256):
        acc = (acc + key[j % length] + out[j]) % 256
        out[j], out[acc] = out[acc], out[j]

    return out

def gimme(enc, flag, flag_len):
    i, j = 0, 0

    fl = flag[:]

    for idx in range(flag_len):
        i = (i + 1) % 256
        j = (j + enc[i]) % 256
        enc[i], enc[j] = enc[j], enc[i]
        k = enc[(enc[i] + enc[j]) % 256]
        fl[idx] = fl[idx] ^ k

    return fl


def to_str(xs):
    return "".join(list(map(lambda x : chr(x), xs)))

flag = [0x6a, 0x0c, 0x93, 0xb0][::-1] + [
    0x24, 0xD9, 0xBC, 0x46, 0xE3, 0xD6, 0xD2, 0x2B,  0xC, 0x7A, 0xD4,
    0x38, 0x52, 0x5B, 0x6C, 0x67, 0x17, 0x71, 0xE0, 0xF4, 0xFB, 0x96,
    0xFF, 0xEA, 0xED, 0x63, 0x2B, 0x4B, 0x4A, 0x5E, 0xEB, 0x9F, 0x42,
    0x65, 0x50, 0xF1, 0x51, 0x3F, 0x52, 0xEA, 0x11, 0x2E, 0xF1, 0x1A,
    0xB0, 0x93, 0x2F, 0xEA, 0xE3, 0x6F,  0xE, 0xAF, 0x42, 0xCF, 0xF7,
    0x37, 0xE4, 0xE6, 0x9F, 0xB6, 0xAD, 0x92, 0xB4,  0xD, 0xF3, 0x39,
    0xD0, 0x6B, 0x5D, 0x7E, 0x86, 0xD9, 0x87, 0xA6, 0x7E, 0x10, 0x33,
    0xE2, 0xEF, 0x1E, 0x15, 0x8F,  0xE, 0xDD, 0x13, 0xE0, 0x31, 0xDF,
    0xEB, 0x44, 0xAF, 0x38, 0xB4, 0xE6, 0x9E, 0xFD
]

from tqdm import tqdm

if __name__ == '__main__':
    for i in tqdm(range(43, 126)):
        for j in tqdm(range(33, 126)):
            for k in tqdm(range(33, 126)):
                for l in range(33, 126):
                    key = [i, j, k, l]
                    out = encode(key, len(key))
                    fl = gimme(out, flag, len(flag))
                    fl = to_str(fl)

                    if fl[:8] == "CNS_CTF{":
                        print(fl)
                        exit(1)


    # key = list(map(lambda x : ord(x), s))
    out = encode(key, len(key))
    fl = gimme(out, flag, len(flag))
    fl = to_str(fl)
    print(fl)



"""
   10728:	e3010337 	movw	r0, #4919	; 0x1337
   1072c:	e59f1014 	ldr	r1, [pc, #20]	; 10748 <main+0xa8>
   10730:	ebffffb3    bl call_me

   48 17 00 E3
   01 10 40 E3
"""
