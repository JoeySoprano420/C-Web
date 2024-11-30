func fibonacci (int n) -> int {
    if (n <= 1) {
        return n;
    }
    /*@active {trace: true, priority: high}*/
    int a = 0, b = 1, c;
    for (int i = 2; i <= n; i++) {
        c = a + b;
        a = b;
        b = c;
    }
    return c;
}
