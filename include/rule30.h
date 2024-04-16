#ifndef A_RULE30
#define A_RULE30

#include "algorithm.h"

class Rule30 : public Algorithm
{
public:
    Rule30(uint64_t seed) : Algorithm(seed){};
    uint64_t peekNext() {
        uint64_t x = this->state;

        x &= 1;
        this->state = (this->state >> 1) ^ (this->state | this->state << 1);

        return x;
    };
};

#endif