#ifndef A_RULE30
#define A_RULE30

#include "algorithm.h"
#include <iostream>
using namespace std;

class Rule30 : public Algorithm
{
private:
    uint64_t row;
public:
    Rule30(uint64_t seed) : Algorithm(seed){
        this->maxValue = 1;
    };
    uint64_t peekNext() {
        uint64_t x;

        switch (this->row & 7) {
            case 0:
            case 5:
            case 6:
            case 7:
                x = 0;
                break;
            case 1:
            case 2:
            case 3:
            case 4:
                x = 1;
                break;
        }

        return x;
    };

    uint64_t next() {
        if (this->row == 0) {
            this->row = this->seed;
        }

        this->state = peekNext();

        this->row >>= 3;

        return this->state;
    }
};

#endif