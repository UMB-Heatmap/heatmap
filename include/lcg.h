//Linear Congruential Generator (LCG) algorithm
#ifndef A_LCG
#define A_LCG

#include "algorithm.h"

class LinConGen : public Algorithm {
public:
    LinConGen(uint64_t seed) : Algorithm(seed) {};
    uint64_t peekNext() {
        uint64_t x = this->state;
        uint64_t mod = 2147483648, mult = 1103515245, inc = 12345;
        x = ((mult * x) + inc) % mod;
        
        return x;
    };
};

#endif