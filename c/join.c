#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

pthread_t a, b, c;

void *tf_c(void *arg) {
	pthread_exit(NULL);
}

void *tf_b(void *arg) {

	pthread_create(&c, NULL, tf_c, NULL);

	pthread_exit(NULL);
}

void *tf_a(void *arg) {

	pthread_create(&b, NULL, tf_b, NULL);

	// make sure c will be running when joining c
	sleep(5);

	printf("[[[[%d]]]]\n", pthread_join(c, NULL));

	pthread_exit(NULL);
}

int main(int argc, char const *argv[])
{

	

	int rc;

	rc = pthread_create(&a, NULL, tf_a, NULL);
	printf("[%d]\n", rc);

	rc = pthread_join(a, NULL);
	printf("[%d]\n", rc);
	rc = pthread_join(b, NULL);
	printf("[%d]\n", rc);
	// rc = pthread_join(c, NULL);
	// printf("[%d]\n", rc);


	return 0;
}