#ifndef A_MIDDLE_SQUARE
#define A_MIDDLE_SQUARE

#include "algorithm.h"

class Middle_Square : public Algorithm {
public:
    Middle_Square(uint64_t seed) : Algorithm(seed) {};
    uint64_t peekNext() {
        uint64_t x = this->state;
        x = x * x;
        std::string squareX = std::to_string(x);
        int midIndex = (squareX.size() / 2) - 2;
        std::string newX = squareX.substr(midIndex, 4);
        x = std::stoull(newX);
        return x;
        
    };
};

#endif