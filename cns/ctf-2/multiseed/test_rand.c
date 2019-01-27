#include <stdlib.h>
#include <stdio.h>

unsigned int seeds[] = {
    0xb19d1c5f, 0xd678b9a7, 0x3d68432d, 0xb78cf1b3,
    0x43e5308b, 0x6d461699, 0x69946081, 0xbdadad6c,
    0x205c11a2,	0x6565a5b0
};

unsigned int flag_enc[] = {
    0xdb, 0x20, 0x98, 0xc1,
    0x08, 0x84, 0x5e, 0xda,
    0xd5, 0xbb, 0x01, 0x85,
    0xf2, 0xb4, 0x8d, 0xb5,
    0x8a, 0x75, 0x98, 0x64,
    0xda, 0x2e, 0xf8, 0x09,
    0x0f, 0xa3, 0x2c, 0xa4,
    0xe9, 0x16, 0x84, 0x46,
    0x80, 0xd9, 0xdb, 0x50
};

unsigned int flag_len = 0x24;

int main(void)
{
    unsigned int input[0x24];

    for (size_t t = 0; t < 10; t++) {
        char *statebuf = calloc(0x80, sizeof(char));
        struct random_data buf;
        int32_t result;

        buf.state = NULL;

        initstate_r(seeds[t], statebuf, 0x80, &buf);
        srandom_r(seeds[t], &buf);

        printf("%zu: [", t);
        for (size_t i = 0; i < flag_len; ++i) {
            random_r(&buf, &result);
            input[i] = (flag_enc[i] ^ result) & 0xff; // keep lsB

            printf("0x%02x, ", input[i]);
        }
        printf("],\n\n");
    }

    return 0;
}
