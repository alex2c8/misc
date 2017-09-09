#include <openssl/aes.h>
#include <stdlib.h>
#include <openssl/opensslconf.h>
#include <stddef.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>


unsigned char encKey[32];
AES_KEY aes_key;

unsigned char buf[16];
unsigned char decString[16];

void genKey(unsigned int t0)
{

}


void decrypt(int inputFD, int outputFD, unsigned int t0)
{

}

int main(int argc, char const *argv[])
{
	int inputFD = open(argv[1], 0, 0x1B4);
	int outputFD = open(argv[2], 0x41, 0x1B4);


	unsigned int t0 = atoi(argv[3]);

	unsigned int bytesRead;

	unsigned int i;

	  srand(t0);

	  for ( i = 0; ; ++i )
	  {
	    if ( i > 31 )
	      break;
	    encKey[i] = rand();
	  }

	AES_set_decrypt_key(encKey, 256, &aes_key);

	do
	{
		memset(&buf, 0, 16);
		bytesRead = read(inputFD, &buf, 16);
		//printf("\tbytes_read = %ul\n", bytesRead);
		if ( !bytesRead )
			break;
		AES_decrypt(buf, decString, &aes_key);
		write(outputFD, decString, 16);

		//printf("\t[%s]\n", decString);

	}  while ( bytesRead > 15 );


	close(inputFD);
	close(outputFD);

	return 0;
}
