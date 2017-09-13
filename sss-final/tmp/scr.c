#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

int main() {
    char *s = NULL;
    char *buf;

    read(open("/dev/urandom", O_RDONLY), (char*)&buf, 4);

    scanf("%lu", &s);

    if(s == buf) {
        puts("DA");
    }

    else {
        puts("NU");
    }
    

    return 0;
}
