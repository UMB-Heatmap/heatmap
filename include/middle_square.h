#ifndef A_MIDDLE_SQUARE
#define A_MIDDLE_SQUARE

#include "algorithm.h"

class Middle_Square : public Algorithm {
public:
    Middle_Square(uint64_t seed) : Algorithm(seed) {};
    uint64_t peekNext() {
        uint64_t x = this->state;
        this->maxValue = 4294967296;

        if (x == 0) return x;

        if (seedLen == 0) seedLen = std::to_string(x).size();

        x = x * x;
        std::string squareX = std::to_string(x);

        if (squareX.size() < seedLen) return stoull(squareX);
        int midIndex = (squareX.size() / 2) - (seedLen/2);
        std::string newX = squareX.substr(midIndex, seedLen);
        x = std::stoull(newX);

        return x;
        
    };

    private:
    int seedLen = 0;
};

#endif