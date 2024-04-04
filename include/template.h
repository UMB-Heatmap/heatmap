// REPLACE XXXXXX and Xxxxxx with names that make sense and delete this comment
#ifndef A_XXXXXX
#define A_XXXXXX

#include "algorithm.h"

class Xxxxxx : public Algorithm {
public:
    Xxxxxx(uint64_t seed) : Algorithm(seed) {};
    uint64_t peekNext() {
        uint64_t x = this->state;

        // YOUR ALGORITHM. Delete this comment.
        
        return x;
    };
};

#endif