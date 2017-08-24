#include <unistd.h>
#include <sys/stat.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <fcntl.h>


int main(void) {

    pid_t kid;

    int ret_code, i;


    char *buf = malloc(20);


    int fd = open("test_file", O_RDONLY, 0644);


    ret_code = dup2(fd, 0);

    read(0, buf, 10);

    printf("[%s]\n", buf);

    //ret_code = dup2(fd,1);
    //ret_code = dup2(fd,2);
    
    //fprintf(stderr, "err\n");
    //fprintf(stdout, "out\n");


   // const char *argv[] = {"qq", NULL};

    /*
    kid = fork();


    if(kid == 0) {
       
        execvp(argv[0], (char*const*)argv);

        fprintf(stderr, "exec error");

        free(x);

        exit(1);
    }
    else {
        printf("{%d}\n", x[0]);
        free(x);

        waitpid(kid, &ret_code, 0);

        if(WIFEXITED(ret_code))
            ret_code = WEXITSTATUS(ret_code);
        else
            ret_code = 1;
    }

    */

    return 0;
}
