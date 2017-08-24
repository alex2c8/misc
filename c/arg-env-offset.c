#include <stdio.h>
#include <stdlib.h>

extern char **environ;

int main(int argc, char **argv)
{
    printf("{%p}\n", environ[0]);
    printf("{%p}\n", argv[argc - 1]);

    unsigned int gap = environ[0] - argv[argc - 1];

    printf("[%d]\n", gap);

    return 0;
}
