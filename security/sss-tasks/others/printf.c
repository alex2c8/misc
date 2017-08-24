#include <stdio.h>

int main() {
	unsigned char foo[4];

	foo[0] = 'A';

	putchar(foo[0]);
	
	printf("%64u%n", 7350, (int *) foo);

	putchar(foo[0]);

	return 0;
}
