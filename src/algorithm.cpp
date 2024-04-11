#include "../include/algorithm.h"

Algorithm::Algorithm(uint64_t seed) {
    this->seed = seed;
    this->state = seed;
    this->maxValue = std::numeric_limits<uint64_t>::max();
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
void Algorithm::setDebug(bool debug) {
    this->debug = debug;
};

// reads from left to right
int getArg_int(std::deque<int> *args) {
    if (args->empty()) {
        throw std::runtime_error("Int deque is empty");
    }
    int res = args->front();
    args->pop_front();
    return res;
}

// reads from left to right
char getArg_char(std::deque<std::string> *args) {
    if (args->empty()) {
        throw std::runtime_error("Char deque is empty");
    }
    char res = args->front()[0];
    args->pop_front();
    return res;
}

// reads from left to right
std::string getArg_string(std::deque<std::string> *args) {
    if (args->empty()) {
        throw std::runtime_error("Char deque is empty");
    }
    std::string res = args->front();
    args->pop_front();
    return res;
}