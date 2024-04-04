#include <stdint.h>
#include <cmath>
#include "LCG.h"

uint64_t lcg(uint64_t seed) {
    uint64_t mod = pow(2, 31), mult = 1103515245, inc = 12345;
    return ((mult * seed) + inc) % mod;
}