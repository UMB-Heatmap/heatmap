#ifndef A_LEHMER
#define A_LEHMER

#include "algorithm.h"

class Lehmer : public Algorithm {
public:
    Lehmer(uint64_t seed) : Algorithm(seed) {};
    uint64_t peekNext() {
        uint64_t x = this->state;

        uint64_t product = x * 48271;
        uint64_t y = (product & 0x7fffffff) + (product >> 31);
        y = (y & 0x7fffffff) + (y >> 31);
        x = y;

        return x;
    };
};

#endif