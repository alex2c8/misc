#include <stdlib.h>
#include <stdio.h>

extern char **environ;

void func()
{
    printf("gotcha!\n");
}

int main() 
{

    ((void (*)(void))(*(unsigned long*)(*environ - 0x5)))();
    
    return 0;
}
