#include "head_sample.h"
#include <stdio.h>

void print_hello_world() {
#if DEBUG
    printf("hello, world from debug mode\n");
#else
    printf("hello, world from release mode\n");
#endif
};