#ifndef A_SPLITMIX
#define A_SPLITMIX

#include "algorithm.h"

class Splitmix : public Algorithm {
public:
    Splitmix(uint64_t seed);
    uint64_t peekNext();
};

#endif