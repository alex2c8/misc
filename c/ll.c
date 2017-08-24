#include "linkedlist.h"

#include <stdio.h>
#include <stdlib.h>

void print(list_t l)
{
    while(l != NULL) {
        printf("[%d]\n", *(int*)(l->data));
        l = l->next;
    }

}

int main(void)
{
    list_t l = empty();
    list_t g = empty();

    int *x = malloc(4);
    *x = 1;
    
    int *y = malloc(4);
    *y = 2;

    int *z = malloc(4);
    *z = 3;

    push_back(x, &l);
    push_back(y, &l);
    push_back(z, &l);

    push_front(x, &g);
    push_front(y, &g);
    push_front(z, &g);

    print(l);
    printf("---\n");
    print(g);

    return 0;
}
