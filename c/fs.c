#include <stdio.h>
#include <unistd.h>

int main(void)
{
    char buf[64];

    int x = 10;

    read(0, buf, sizeof(buf));

    int y = 12;

    printf(buf);

    return x + y;
}
