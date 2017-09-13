#include <stdlib.h>
#include <stdio.h>

void * write_uchar(void *b)
{
	unsigned char *buf = b;
	buf[0] = rand();
	printf("Unsigned char: %d\n", buf[0]);
	return &buf[1];
}

void * write_schar(void *b)
{
	signed char *buf = b;
	buf[0] = rand();
	printf("Signed char: %d\n", buf[0]);
	return &buf[1];
}

void * write_ushort(void *b)
{
	unsigned short *buf = b;
	buf[0] = rand();
	printf("Unsigned short: %d\n", buf[0]);
	return &buf[1];
}

void * write_sshort(void *b)
{
	signed short *buf = b;
	buf[0] = rand();
	printf("Signed short: %d\n", buf[0]);
	return &buf[1];
}

void * write_uint(void *b)
{
	unsigned int *buf = b;
	buf[0] = rand();
	printf("Unsigned int: %d\n", buf[0]);
	return &buf[1];
}

void * write_sint(void *b)
{
	signed int *buf = b;
	buf[0] = rand();
	printf("Signed int: %d\n", buf[0]);
	return &buf[1];
}

void seed_rng()
{
        struct timeval time;
        gettimeofday(&time, NULL);
        srand(time.tv_usec);
}

int main()
{
	int i;
        setbuf(stdout, NULL);

	unsigned char buf[1000];
	void *p = buf;
	void *funcs[] = {write_uchar, write_schar, write_ushort, write_sshort, write_uint, write_sint};
	void* (*f)(void*) = NULL;

	seed_rng();

	for (i = 0 ; i < 16; i++ ){
		f = funcs[rand() % 4] ;
		p = f(p);
	}
	int diff = (unsigned char *)p - buf;
	diff = diff / 4;

	for (i = 0 ; i < diff; i++){
		unsigned int user_input;
		printf("Input dword %d in hex\n", i);
		scanf("%x\n", &user_input);
		if (user_input != ((unsigned int *)buf)[i]) {
			printf("Wrong!\n");
			exit(-1);
		}
	}

	printf("Well done!\n");
	system("/bin/sh");
	return 0;
}
