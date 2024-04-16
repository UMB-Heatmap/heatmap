#ifndef A_MIDDLE_SQUARE
#define A_MIDDLE_SQUARE

#include "algorithm.h"

class Middle_Square : public Algorithm {
public:
    Middle_Square(uint64_t seed) : Algorithm(seed) {};
    uint64_t peekNext() {
        uint64_t x = this->state;

        if (x == 0) return x;

        x = x * x;
        std::string squareX = std::to_string(x);
        
        if (squareX.size() < 4) return stoull(squareX);
        int midIndex = (squareX.size() / 2) - 2;
        std::string newX = squareX.substr(midIndex, 4);
        x = std::stoull(newX);
        return x;
        
    };
};

#endif