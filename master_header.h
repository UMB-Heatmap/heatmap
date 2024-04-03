#include <iostream>
#include <fstream>
#include <string>
#include <stdint.h>
#include <unistd.h>
#include <string.h>

#include "include/algorithm.h"
#include "include/xorshift64.h"
#include "include/splitmix.h"

#define XORSHIFT 1
#define SPLITMIX 2

std::unordered_map<std::string, int> algorithmMap = {
    {"xorshift", XORSHIFT},
    {"splitmix", SPLITMIX},
};

struct params {
    int algo;
    int n;
    uint64_t seed;
    bool debug;
    bool isOutFile;
    std::string outFile;
};

Algorithm * getAlgorithm(int algorithm, uint64_t seed) {
    Algorithm * algo = nullptr;
    switch (algorithm) {
        case XORSHIFT:
            algo = new XorShift64(seed);
        case SPLITMIX:
            algo = new Splitmix(seed);
        default:
            algo = new XorShift64(seed);
    }
    return algo;
}

int getAlgorithmNum(std::string algorithm) {
    auto item = algorithmMap.find(algorithm);
    if (item != algorithmMap.end()) {
        return item->second;
    }
    return XORSHIFT;
};

