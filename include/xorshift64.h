#ifndef A_XORSHIFT64
#define A_XORSHIFT64

#include "algorithm.h"

class XorShift64 : public Algorithm {
public:
    XorShift64(uint64_t seed) : Algorithm(seed) {};
    uint64_t peekNext() {
        uint64_t x = this->state;
        x ^= x << 13;
        x ^= x >> 7;
        x ^= x << 17;
        return x;
    };
};

#endif