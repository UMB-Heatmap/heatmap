#ifndef XORSHIFT64
#define XORSHIFT64

#include "algorithm.h"

class XorShift64 : public Algorithm {
public:
    XorShift64(uint64_t seed);
    uint64_t peekNext();
};

#endif