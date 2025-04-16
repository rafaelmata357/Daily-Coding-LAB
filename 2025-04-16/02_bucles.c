// Implementación de bucles for, while y do-while.

#include <stdio.h>

int main() {
    int i;

    // Bucle for
    printf("Bucle for:\n");
    for (i = 1; i <= 5; i++) {
        printf("%d ", i);
    }
    printf("\n");

    // Bucle while
    printf("Bucle while:\n");
    i = 1;
    while (i <= 5) {
        printf("%d ", i);
        i++;
    }
    printf("\n");

    // Bucle do-while
    printf("Bucle do-while:\n");
    i = 1;
    do {
        printf("%d ", i);
        i++;
    } while (i <= 5);
    printf("\n");

    return 0;
}
