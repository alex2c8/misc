#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    
    
    printf("8: %lu\n", sizeof(int8_t));
    printf("16: %lu\n", sizeof(int16_t));
    printf("32: %lu\n", sizeof(int32_t));
    printf("64: %lu\n", sizeof(int64_t));
    printf("int: %lu\n", sizeof(int));
    printf("uint: %lu\n", sizeof(unsigned int));
    

    //int64_t i64 = 9223372036854775808;

    //printf("%lld\n", i64);


    int *v = malloc(10 * sizeof(int));
    int x = 101;

    memset(v, 1, 10 * sizeof(int));

    for(int i = 0; i < 10; i++) {
        printf("[%d]\n", *(v+i));
    }

    return 0;
}