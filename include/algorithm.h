#ifndef A_ALGORITHM
#define A_ALGORITHM

#include <iostream>
#include <fstream>
#include <string>
#include <stdint.h>
#include <unistd.h>
#include <string.h>

class Algorithm {
public:
    Algorithm(uint64_t seed);
    virtual ~Algorithm();
    virtual uint64_t peekNext() = 0;
    uint64_t next();
    uint64_t getSeed();
    uint64_t getState();
    void setSeed(uint64_t seed);
    void setDebug(bool debug);

protected:
    uint64_t seed;
    uint64_t state;
    bool debug;
};

#endif