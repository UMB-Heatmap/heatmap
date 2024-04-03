#ifndef A_XORSHIFT64
#define A_XORSHIFT64

#include "algorithm.h"

class XorShift64 : public Algorithm {
public:
    XorShift64(uint64_t seed);
    uint64_t peekNext();
};

#endif