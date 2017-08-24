#include <stdio.h>
#include <pthread.h>

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

int x = 0;

void *func(void *arg)
{
    pthread_mutex_lock(&mutex);
    
    x = x + 1;

    pthread_mutex_unlock(&mutex);

    pthread_exit(NULL);
}

int main(void)
{
    pthread_t tid;

    pthread_create(&tid, NULL, (void*)func, NULL);

    pthread_join(tid, NULL);

    printf("[%d]", x);
    
    return 0;
}
