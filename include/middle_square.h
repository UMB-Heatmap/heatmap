#ifndef A_MIDDLE_SQUARE
#define A_MIDDLE_SQUARE

#include "algorithm.h"

class Middle_Square : public Algorithm {
public:
    Middle_Square(uint64_t seed) : Algorithm(seed) {};
    uint64_t peekNext() {
        uint64_t x = this->state;
        //this->maxValue = 9223372036854775807;

        if (x == 0) return x;

        if (seedLen == 0) seedLen = std::to_string(x).size();
        std::string maxVal = "";
        for (int i = 0; i < seedLen; i++){
            maxVal = maxVal + "9";
        }
        this->maxValue = std::stoull(maxVal);

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