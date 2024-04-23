#ifndef A_BLUMBLUMSHUB
#define A_BLUMBLUMSHUB

#include "algorithm.h"

class BlumBlumShub : public Algorithm {
public:
    BlumBlumShub(uint64_t seed, std::deque<int> algOpt_int) : Algorithm(seed) {
        try { // if p and q are not provided
            this->p = getArg_int(&algOpt_int);
            this->q = getArg_int(&algOpt_int); 
        } catch (const std::runtime_error &err) {
            throw std::runtime_error("Missing options: p, q");
        }
    };

    bool isBlumPrime(int n) { // check if n is a Blum Prime
        if (n % 4 != 3) { // check if n is congruent to 3 mod 4
            return false;
        }
        for (int i = 2; i < n; i++) { // check if n is prime
            if (n % i == 0) {
                return false;
            }
        }
        return true;

    if (!isBlumPrime(p)) { // check if p is a Blum Prime
        throw std::runtime_error("p must be a Blum Prime");
        }

    if (!isBlumPrime(q)) { // check if q is a Blum Prime
        throw std::runtime_error("q must be a Blum Prime");
        }
    };
    
    uint64_t peekNext() { // Blum Blum Shub algorithm
        uint64_t x = this->state;
        
        uint64_t m = p * q;
        x = (x * x) % m;
        
        return x;
    };

private:
    int p;
    int q;
};

#endif