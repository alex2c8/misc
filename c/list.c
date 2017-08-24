#include <stdlib.h>
#include <stdio.h>

#include <pthread.h>


/*
 * Dangers of manipulating a list without synchronization mechanisms
 * Will throw sigsegv
 */

typedef struct cell {
    int val;
    struct cell *next;
} cell_t, *list_t;

pthread_t t1, t2;

list_t list = NULL;


void consume(list_t l)
{
    while (l != NULL)
        l = l->next;
}

void consume_side_effect(list_t *l)
{
    while (*l != NULL)
        *l = (*l)->next;
}

void add(list_t *l)
{
    list_t x = *l;

    while(x != NULL) {
        if(x->val % 2 == 0)
            x->val = 1337;
        x = x->next;
    }
}

void add_side_effect(list_t *l)
{
    while(*l != NULL) {
        if ((*l)->val % 2 == 0)
            (*l)->val = 1337;
        *l = (*l)->next;
    }
}

// t1 just traverses the struct
void *t1_func(void *arg)
{
    consume_side_effect(&list);

    pthread_exit(NULL);
}

void *t2_func(void *arg)
{
    //add_side_effect(&list);
    add(&list);

    pthread_exit(NULL);
}

list_t new(int x)
{
    list_t aux = calloc(1, sizeof(cell_t));

    aux->val = x;

    aux->next = NULL;

    return aux;
}

list_t cons(int x, list_t rest)
{
    list_t aux = new(x);

    aux->next = rest;

    return rest = aux;
}



int main(void)
{

    int i;

    int n = 1000000;

    for (i = n; i >= 1; i--) {
        list = cons(i, list);
    }


    pthread_create(&t1, NULL, (void *)t1_func, NULL);
    pthread_create(&t2, NULL, (void *)t2_func, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("[%d]\n", list->next->val);

    //consume_side_effect(&list);

    //printf("[%d]\n", list->next->next->val);
    printf("[%d]\n", list == NULL);


    free(list);

    return 0;
}
