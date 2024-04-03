#include "xorshift64.h"

XorShift64::XorShift64(uint64_t seed) : Algorithm(seed) {};
uint64_t XorShift64::peekNext() {
    if (this->debug) std::cout << "Performing xorshift64 operation... ";
    uint64_t x = this->state;
    uint64_t result = (x += 0x9E3779B97f4A7C15);
    result = (result ^ (result >> 30)) * 0xBF58476D1CE4E5B9;
    result = (result ^ (result >> 27)) * 0x94D049BB133111EB;
    return result ^ (result >> 31);
};