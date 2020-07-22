#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#include <stdint.h>
#include "dulp.c"
/*

gcc bench.c \
-Wall \
-Wextra \
-pedantic \
-Werror \
-std=c99 \
-O3 \
-march=native \
-o bench && perf record ./bench


perf report


*/

clock_t
test(double* restrict x,
     double* restrict y,
     float* restrict z,
     size_t n)
{
    clock_t start, end;
    start = clock();
    for (size_t i = 0; i < 500; ++i) {
        for (size_t j = 0; j < n; ++j) {
            z[j] = dulp(x[j], y[j]);
        }
        // prevent compiler reduction
        while(z[0] == 0.5) {
             x[i] += 1.;
             y[i] += 1.;
        }
    }
    end = clock();
    return end - start;
}


void
runtest(size_t n)
{
    double* x;
    double* y;
    float* z;
    srand(1234);

    x = (double*)malloc(n*sizeof(*x));
    for (size_t i = 0; i < n; ++i)
        x[i] = (rand() + 0.5)/((uint64_t)RAND_MAX + 1) - 0.5;
    y = (double*)malloc(n*sizeof(*y));
    for (size_t i = 0; i < n; ++i)
        y[i] = (rand() + 0.5)/((uint64_t)RAND_MAX + 1) - 0.5;
    z = (float*)malloc(n*sizeof(*z));

    printf("Running double test");
    clock_t res1;
    res1 = test(x, y, z, n);
    printf("warmup took %ld clocks\n", res1);
    for (int i = 0; i < 3; ++i) {
        res1 = test(x, y, z, n);
        printf("dulp  %ld clocks\n", res1);
        // prevent compiler reduction
        while(z[0] == 0.5) {}
    }

    free(x);
    free(y);
    free(z);
}


clock_t
testf(float* x,
      float* y,
      float* z,
      size_t n)
{
    clock_t start, end;
    start = clock();
    for (size_t i = 0; i < 500; ++i) {
        for (size_t j = 0; j < n; ++j) {
            z[j] = dulpf(x[j], y[j]);
        }
        // prevent compiler reduction
        while(z[0] == 0.5) {
             x[i] += 1.;
             y[i] += 1.;
        }
    }
    end = clock();
    return end - start;
}


void
runtestf(size_t n)
{
    float *x, *y, *z;
    srand(1234);

    x = (float*)malloc(n*sizeof(*x));
    for (size_t i = 0; i < n; ++i)
        x[i] = (rand() + 0.5f)/((uint64_t)RAND_MAX + 1) - 0.5f;
    y = (float*)malloc(n*sizeof(*y));
    for (size_t i = 0; i < n; ++i)
        x[i] = (rand() + 0.5f)/((uint64_t)RAND_MAX + 1) - 0.5f;
    z = (float*)malloc(n*sizeof(*z));

    puts("Running float test");
    clock_t res1;
    res1 = testf(x, y, z, n);
    printf("warmup took %ld clocks\n", res1);
    for (int i = 0; i < 3; ++i) {
        res1 = testf(x, y, z, n);
        printf("dulpf %ld clocks\n", res1);
        // prevent compiler reduction
        while(z[0] == 0.5) {}
    }

    while(z[0] == 0.5) {}

    free(x);
    free(y);
    free(z);
}

int
main()
{
    runtest(1000*1000);
    runtestf(1000*1000);
}
