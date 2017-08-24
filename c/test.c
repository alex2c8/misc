#include <stdio.h>
#include <stdlib.h>
#include <string.h>


void xor(char *s, int len) {
    int i;

    for (i = 0; i < len; i++)
            *(s + i) ^= 1;
}


int main(int argc, char *argv[])
{
    char *s = strdup(argv[1]);

    xor(s, strlen(s));

    printf("[%s]\n", s);

	return 0;
}
