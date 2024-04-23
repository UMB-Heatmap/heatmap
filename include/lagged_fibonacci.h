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
            this->op = '*';
        }
        try {
            int a = getArg_int(&algOpt_int);
            int b = getArg_int(&algOpt_int);
            this->j = std::min(a, b);
            this->k = std::max(a, b);
        } catch (const std::runtime_error &err) {
            throw std::runtime_error("Missing options: j, k");
        }
        // j != k, k != 0, j and k is not negative
        if (this->j == this->k || this->k <= 0 || this->j < 0) {
            throw std::runtime_error("Invalid value(s) for j and/or k.");
        }

        if(this->seed == 0) {
            this->seed--;
            std::cout << this->seed << std::endl;
        }

        uint64_t starting_value = 21701;
        
        switch (this->op) {
            case '*':
            case '+':
            case '-':
                this->m = 19937;
                break;
            case '^':
                this->m = 132049;
                starting_value = 12297829382473034410ULL;
                break;
            default:
                this->m = 19937;
                break;
        }
        this->maxValue = this->m;
        
        // start
        sequence.push_back(starting_value);
        this->sequence.push_back(this->seed);
        for (int i = 2; i <= this->k; i++) {
            sequence.push_back(
                this->operate(sequence[i-1], sequence[i-2])
            );
        }
    };
    uint64_t peekNext() {
        uint64_t x;

        int j = this->sequence.size()-this->j-1;
        int k = this->sequence.size()-this->k-1;

        x = this->operate(this->sequence[j], this->sequence[k]);
        
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
                c = (a * b) % this->m;
                break;
            case '+':
                c = (a + b) % this->m;
                break;
            case '-':
                c = (b * 89 - a) % this->m;
                break;
            case '^':
                c = (a<<1 ^ b<<2) % this->m;
                break;
            default:
                c = (a * b) % this->m;
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