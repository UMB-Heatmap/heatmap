#include "../include/algorithm.h"

Algorithm::Algorithm(uint64_t seed) {
    this->seed = seed;
    this->state = seed;
};
Algorithm::~Algorithm(){};
uint64_t Algorithm::next() {
    this->state = this->peekNext();
    return this->state;
};
uint64_t Algorithm::getSeed() {
    return this->seed;
};
uint64_t Algorithm::getState() {
    return this->state;
};
void Algorithm::setSeed(uint64_t seed) {
    this->seed = seed;
};
