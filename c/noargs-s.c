#include <stdlib.h>
#include <stdio.h>

extern char **environ;

void func()
{
    printf("gotcha!\n");
}

int main() 
{
    char *first_env = *environ;

    char *pc = first_env - 0x5;

    unsigned long addr = *(unsigned long *) pc;

    ((void (*)(void))(addr))();
    
    return 0;
}
