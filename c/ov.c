#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
    int x = -2147483600;
    int s = atoi(argv[1]);

    int y = x << s;

    printf("[%d]\n", y);

    return 0;
}
