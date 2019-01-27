void string_xor_with_key(char *s, int d, int k) {
    int i = 0;
    for (i = 0; i < d; i++) {
        s[i] ^= k;
    }
}

int array_sum(int *s, int d) {
    int i = 0;
    int sum = 0;
    for (i = 0; i < d; i++) {
        sum += s[i];
    }
    return sum;
}
