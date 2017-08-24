#include <stdlib.h>
#include <sys/time.h>
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/wait.h>

void parrot(int sockfd)
{
	int count;
	char buf[1024];
	dprintf(sockfd, "==============================================\n");
	dprintf(sockfd, "Welcome to the Unexploitable Parrot service\n");
	dprintf(sockfd, "==============================================\n");

	dprintf(sockfd, "Stack smashing is futile if you apply protection mechanisms, right? Can you prove me wrong?\n");
	dprintf(sockfd, "Here, have a stack buffer overflow. It's on us :)\n");
	count = read(sockfd, buf, 1200);
}


void doprocessing(int sockfd)
{
	parrot(sockfd);
	dprintf(sockfd, "Goodbye!\n");
}

int main(int argc, char **argv)
{
    int optval = 1;
    int sockfd, newsockfd, portno;
    socklen_t clilen;
    struct sockaddr_in serv_addr, cli_addr;

    if (argc != 2) {
	printf("Usage: %s <port>\n", argv[0]);
	exit(0);
    }

    portno = atoi(argv[1]);


    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0)
    {
        perror("ERROR opening socket");
        exit(1);
    }

    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;

    serv_addr.sin_addr.s_addr = inet_addr("0.0.0.0");
    serv_addr.sin_port = htons(portno);
    setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof optval);

    if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0)
    {
         perror("ERROR on binding");
         exit(1);
    }

    listen(sockfd, 5);
    clilen = sizeof(cli_addr);
    while (1)
    {
    int pid;
    newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
    if (newsockfd < 0)
    {
        perror("ERROR on accept");
        exit(1);
    }
    pid = fork();
    if (pid < 0)
    {
        perror("ERROR on fork");
    	exit(1);
    }
    if (pid == 0)
    {
        close(sockfd);
        doprocessing(newsockfd);
        exit(0);
    } else {
        waitpid(-1, NULL, WNOHANG);
        close(newsockfd);
    }
    }
}
