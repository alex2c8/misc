#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

#define NUM_ARGS 1
#define LAST_ARG NUM_ARGS+1

int main(int argc, char **argv)
{
	int i;

	char *args[NUM_ARGS + 2];

	args[0] = strdup(argv[1]);
	args[1] = strdup("\xd0\x55\x55\x56");

	args[LAST_ARG] = NULL;

    /*
	printf("calling: ");
	for (i = 0; i < LAST_ARG; i++)
		printf("[%s] ", args[i]);
	printf("\n");
    */

	execv(args[0], args);

	fprintf(stderr, "error\n");

	return 0;
}
