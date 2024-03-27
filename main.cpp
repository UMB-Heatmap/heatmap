#include <iostream>
#include <fstream>
#include <string>
// en.wikipedia.org/wiki/Xorshift

// #include <gsl/gsl_sf_bessel.h>
/*
void testGSL() {
    double x = gsl_sf_bessel_J0(5.0);
    std::cout << x << "\n";
}
 */
struct xorshift32_state {
    uint32_t s;
};
struct splitmix64_state {
    uint64_t s;
};
uint64_t splitmix64(splitmix64_state *state) {
    uint64_t result = (state->s += 0x9E3779B97f4A7C15);
    result = (result ^ (result >> 30)) * 0xBF58476D1CE4E5B9;
    result = (result ^ (result >> 27)) * 0x94D049BB133111EB;
    return result ^ (result >> 31);
}
uint32_t xorshift32(xorshift32_state *state) {
    uint32_t x = state->s;
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    return state->s = x;
}
void xorshift32_init(xorshift32_state *state, uint64_t seed) {
    struct splitmix64_state smstate = {seed};
    uint64_t tmp = splitmix64(&smstate);
    state->s = (uint32_t) tmp;
}
uint32_t randomInt32bit(uint64_t seed) {
    xorshift32_state state = {};
    xorshift32_init(&state, seed);
    xorshift32(&state);
    return state.s;
}
uint32_t randomInt32bit(uint64_t seed, xorshift32_state *customState) {
    xorshift32_init(customState, seed);
    xorshift32(customState);
    return customState->s;
}

int randomInt(int lo, int hi, uint64_t seed) {
    float randScalar = (float) randomInt32bit(seed) / (float) 0xFFFFFFFF;
    int num = (int (randScalar * ((float) hi - (float) lo))) + lo;
    return num;
}
int randomInt(int lo, int hi) {
    uint64_t defaultSeed = 0; // DEFAULT SEED
    return randomInt(lo, hi, defaultSeed);
}
int scaleState32bit(int lo, int hi, uint32_t state) {
    // std::cout << "Scaling State: " << state << " to range " << lo << "-" << hi << ". ";
    double randScalar = ((double) state) / ((double) 0xFFFFFFFF);
    int num = (int (randScalar * ((double) hi - (double) lo))) + lo;
    // std::cout << "Returning value: " << num << " ";
    return num;
}
int* randomIntArray(int lo, int hi, uint64_t seed, int numStates) {
    int* nums = (int*) malloc(sizeof(int) * numStates);
    xorshift32_state currentState = {};
    xorshift32_init(&currentState, seed);
    for (int i = 0; i < numStates; i++) {
        int num = scaleState32bit(lo, hi,  xorshift32(&currentState));
        // std::cout << "nums[" << i << "] = " << num << "\n";
        nums[i] = num;
    }
    return nums;
}
struct point2D {
    int x;
    int y;
};
struct colorRGB {
    int r;
    int g;
    int b;
};
point2D randomPoint(int min_X, int min_Y, int max_X, int max_Y, uint64_t seed) {
    int x = randomInt(min_X, max_X, seed);
    int y = randomInt(min_Y, max_Y, seed);
    return {x, y};
}
point2D randomPoint(int min_X, int min_Y, int max_X, int max_Y) {
    int x = randomInt(min_X, max_X);
    int y = randomInt(min_Y, max_Y);
    return {x, y};
}
colorRGB randomColorRGB(uint64_t seed) {
    int r = randomInt(0, 256, seed++);
    int g = randomInt(0, 256, seed++);
    int b = randomInt(0, 256, seed);
    return {r, g, b};
}

bool inCircle(point2D *p, point2D *c, int r) {
    return sqrt(pow(abs(p->x - c->x), 2) + pow(abs(p->y - c->y), 2)) < r;
}
void circleTest(int radius, int numPoints) {
    int numInCircle = 0;
    point2D center = {radius, radius};
    auto* points = (point2D*) malloc(sizeof(point2D) * numPoints);
    for (int i = 0; i < numPoints; i++) {
        points[i] = randomPoint(0, 0, radius*2, radius*2, i);
        if (inCircle(&points[i],  &center, radius)) { numInCircle++; }
    }
    free(points);
    float pi = 4 * ((float) numInCircle) / ((float) numPoints);
    std::cout << "Pi Estimate for XORshift32 with " << numPoints << " total points: " << pi;
}
void buildRandom2DArrayOutput(int seed, int lo, int hi, int numCols, int numRows, std::string *outfile) {
    std::ofstream output;
    output.open(*outfile);
    for (int i = 0; i < numRows; i++) {
        int* nums = randomIntArray(lo, hi, seed++, numCols);
        for (int j = 0; j < numCols; j++) {
            output << nums[j];
            if (j != numCols - 1) { output << " "; }
        }
        free(nums);
        output << "\n";
    }
    output.close();
}

int main() {
    std::string outfileName = "random2DArray.out";
    buildRandom2DArrayOutput(1, 0, 256, 100, 100, &outfileName);
    circleTest(1000, 10000);
    return 0;
}
