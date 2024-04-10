#include <iostream>
#include <fstream>
#include <string>
#include <stdint.h>
#include <unistd.h>
#include <string.h>
#include "algorithm.h"

// ADD HEADER HERE
#include "xorshift64.h"
#include "splitmix.h"
#include "lehmer.h"
#include "lcg.h"

// ADD INDEX HERE
#define XORSHIFT    1
#define SPLITMIX    2
#define LEHMER      3
#define LCG         4

// ADD COMMAND LINE NAME HERE
std::unordered_map<std::string, int> algorithmMap = {
    {"xorshift",    XORSHIFT},
    {"splitmix",    SPLITMIX},
    {"lehmer",      LEHMER},
    {"lcg",         LCG}
};

Algorithm * getAlgorithm(int algorithm, uint64_t seed) {
    Algorithm * algo = nullptr;
    switch (algorithm) {
        // ADD CASE HERE
        case XORSHIFT:
            algo = new XorShift64(seed);
            break;
        case SPLITMIX:
            algo = new Splitmix(seed);
            break;
        case LEHMER:
            algo = new Lehmer(seed);
            break;
        case LCG:
            algo = new LinConGen(seed);
            break;

        default:
            algo = new XorShift64(seed);
            break;
    }
    return algo;
}

// DO NOT MODIFY ANYTHING BELOW THIS LINE
// UNLESS YOU KNOW WHAT YOU ARE DOING

struct params {
    int algo;
    int n;
    uint64_t seed;
    bool debug;
    bool isOutFile;
    std::string outFile;
};

int getAlgorithmNum(std::string algorithm) {
    auto item = algorithmMap.find(algorithm);
    if (item != algorithmMap.end()) {
        return item->second;
    }
    // Default Value
    return XORSHIFT;
};
