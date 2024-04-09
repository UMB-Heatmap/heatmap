/*#include "lehmer.h"
#include "algorithm.h"

Lehmer::Lehmer(uint64_t seed) {
    this->state = seed;
    
}
uint64_t Lehmer::peekNext() {
    inline uint32_t lehmer(uint32_t* state) {
    uint64_t product = (uint64_t)*state * 48271;
    uint32_t x = (product & 0x7fffffff) + (product >> 31);
    x = (x & 0x7fffffff) + (x >> 31);
    return *state = x;
}
*/