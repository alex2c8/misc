#include <stdio.h>
#include <stdlib.h>

struct s {
    int v[100];
};

struct s ss;

int main(void)
{
    printf("[%d]\n", sizeof(struct s));

    //struct s *ss = malloc(sizeof(struct s));
    
    //free(ss);
    return 0;
}
