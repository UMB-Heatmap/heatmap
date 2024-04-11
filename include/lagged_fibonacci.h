#ifndef A_LAGGED_FIBO
#define A_LAGGED_FIBO

#include "algorithm.h"

class LaggedFibonacci : public Algorithm {
public:
    LaggedFibonacci(uint64_t seed, std::deque<int> algOpt_int, std::deque<std::string> algOpt_string) : Algorithm(seed) {
        // get 2 seeds from seed
        this->seed = seed;
        this->state = seed;

        try {
            this->op = getArg_char(&algOpt_string);
        } catch (const std::runtime_error &err) {
            throw err;
        }
        try {
            this->j = getArg_int(&algOpt_int);
            this->k = getArg_int(&algOpt_int);
        } catch (const std::runtime_error &err) {
            throw std::runtime_error("Missing options: j, k");
        }

        try {
            this->m = getArg_int(&algOpt_int);
        } catch (const std::runtime_error &err) {
            this->m = 2147483647;
        }

        this->maxValue = this->m;

        // start
        this->sequence.push_back(seed);
        for (int i = 1; i <= std::max(j, k); i++) {
            sequence.push_back(
                this->operate(16807, sequence[i-1]) % m
            );
        }
    };
    uint64_t peekNext() {
        uint64_t x;

        int j = this->sequence.size()-this->j-1;
        int k = this->sequence.size()-this->k-1;

        x = this->operate(this->sequence[j], this->sequence[k]) % this->m;
        
        return x;
    };
    uint64_t next() {
        uint64_t next = this->peekNext();
        this->sequence.push_back(next);
        this->state = this->sequence.back();
        this->sequence.pop_front();
        return this->state;
    };
    uint64_t operate(uint64_t a, uint64_t b) {
        uint64_t c;
        switch (this->op) {
            case '*':
                c = a * b;
                break;
            case '+':
                c = a + b;
                break;
            case '-':
                c = a - b;
                break;
            case '^':
                c = a ^ b;
                break;
            default:
                c = a * b;
                break;
        }
        return c;
    };

private:
    std::deque<uint64_t> sequence;
    char op;
    int j;
    int k;
    int m;
};


#endif