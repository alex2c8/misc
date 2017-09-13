#include <stdio.h>
#include <stdlib.h>

int main() {
    srand(17);

    char *buf = calloc(30, sizeof(char));

  buf[0] = 32;
  buf[1] = 62;
  buf[2] = 2;
  buf[3] = 73;
  buf[4] = 99;
  buf[5] = 11;
  buf[6] = 123;
  buf[7] = 8;
  buf[8] = 5;
  buf[9] = 65;
  buf[10] = 1;
  buf[11] = 53;
  buf[12] = 39;
  buf[13] = 6;
  buf[14] = 111;
  buf[15] = 56;
  buf[16] = 121;
  buf[17] = 33;
  buf[18] = 122;
  buf[19] = 95;
  buf[20] = 1;
  buf[21] = 99;
  buf[22] = 104;
  buf[23] = 113;
  buf[24] = 103;
  buf[25] = 78;

    int i;
    for(i = 0; i <= 25; i++) {
        char x = buf[i] ^ (rand() % 77 + 48);
        printf("%c", x);
    }
    printf("\n");
    return 0;
}
