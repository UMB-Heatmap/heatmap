#ifndef A_ALGORITHM
#define A_ALGORITHM

#include <iostream>
#include <fstream>
#include <string>
#include <stdint.h>
#include <deque>
#include <string.h>
#include <unistd.h>

class Algorithm {
public:
    Algorithm(uint64_t seed);
    virtual ~Algorithm();
    virtual uint64_t peekNext() = 0;
    virtual uint64_t next();
    uint64_t getSeed();
    uint64_t getState();
    void setSeed(uint64_t seed);
    void setDebug(bool debug);
    uint64_t maxValue;

protected:
    uint64_t seed;
    uint64_t state;
    bool debug;
};


int getArg_int(std::deque<int> *args);
char getArg_char(std::deque<std::string> *args);
std::string getArg_string(std::deque<std::string> *args);

#endif