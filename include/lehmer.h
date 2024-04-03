#ifndef A_LEHMER
#define A_LEHMER

#include "algorithm.h"

class Lehmer : public Algorithm {
public:
    Lehmer(uint64_t seed) : Algorithm(seed) {};
    uint64_t peekNext() {
        uint64_t x = this->state;

        uint64_t product = this->state * 48271;
        uint64_t x = (product & 0x7fffffff) + (product >> 31);
        x = (x & 0x7fffffff) + (x >> 31);

        return x;
    };
};

#endif