#include <stdlib.h>
#include <string.h>

void foo() {
	system("/bin/sh");
}

int main(int argc, char** argv) {

	char buffer[60];
	strcpy(buffer, argv[1]);

	return 0;
}
