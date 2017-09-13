#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

#define NUM_ARGS 100
#define VULN "input"

int main(void)
{
	int i, sts;

	char *arg[NUM_ARGS + 1];

	arg[0] = VULN;

	for (i = 1; i < NUM_ARGS; i++)
		arg[i] = "x";

	arg[100] = NULL;

	arg['A'] = "\x00";
	arg['B'] = "\x20\x0a\x0d";


	pid_t vulnp;

	vulnp = fork();

	// vulnerable process
	if (vulnp == 0) {
		execv("./input", arg);
		// TODO
	}

	// parent process
	else {
		wait(&sts);
		printf("[%d]", sts);
	}

	return 42;
}
