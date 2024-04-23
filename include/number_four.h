#ifndef A_FOUR
#define A_FOUR

#include "algorithm.h"

class NumberFour : public Algorithm {
public:
    NumberFour(uint64_t seed) : Algorithm(seed) {
        this->maxValue = 1;
        this->seed = 4; 
        this->state = 4;
    };
    uint64_t peekNext() {
        return 4;
    };
};

#endif