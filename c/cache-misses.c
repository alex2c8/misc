#include <stdio.h>
#include <stdlib.h>

#define N 100

int main(void) {

    int i, j;
    
    int **a = calloc(N, sizeof(int*));
    int **b = calloc(N, sizeof(int*));

    for (i = 0; i < N; i++) {
        a[i] = calloc(N, sizeof(int));
        b[i] = calloc(N, sizeof(int));
    }

    /*
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            a[i][j] = 7;
            //b[i][j] = 10;
        }
    }
    */

    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            a[j][i] += 2;
        }
    }


    

    return 0;
}
