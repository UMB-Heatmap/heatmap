#include <iostream>
#include <fstream>
#include <string>
#include <stdint.h>
#include <unistd.h>
#include <string.h>

#define XORSHIFT 1
#define SPLITMIX 2

int debug = 0;
int isOutFile = 0;
std::string outFile;

struct params {
    int algo;
    uint64_t seed;
    int n;
};

class PRNGStream {
    private:
        uint64_t seed;
        uint64_t state;
        int algo;

        // en.wikipedia.org/wiki/Xorshift
        uint64_t xorshift64() {
            if (debug) std::cout << "Performing xorshift64 operation... ";
            uint64_t x = this->state;
            x ^= x << 13;
            x ^= x >> 7;
            x ^= x << 17;
            return x;
        }
        uint64_t splitmix64() {
            if (debug) std::cout << "Performing splitmix64 operation... ";
            uint64_t x = this->state;
            uint64_t result = (x += 0x9E3779B97f4A7C15);
            result = (result ^ (result >> 30)) * 0xBF58476D1CE4E5B9;
            result = (result ^ (result >> 27)) * 0x94D049BB133111EB;
            return result ^ (result >> 31);
        }
        uint64_t nextState() {
            if (debug) std::cout << "Moving to next state... ";
            switch (this->algo) {
                case 1:
                    return xorshift64();
                case 2:
                    return splitmix64();
                default:
                    return splitmix64();
            }
        }

    public:
        PRNGStream(uint64_t seed, int algo) {
            if (debug) std::cout << "Constructing PRNGStream Object... \n";
            this->seed = seed;
            this->algo = algo;
            this->state = seed;
            this->state = nextState();
        }
        float next() {
            this->state = nextState();
            float randScalar = ((float) this->state / (float) std::numeric_limits<uint64_t>::max()); 
            return randScalar;
        }
        uint64_t getState() {
            return this->state;
        }
        std::string getAlgo() {
            return (this->algo == SPLITMIX) ? "splitmix" : "xorshift";
        }
        uint64_t getSeed() {
            return this->seed;
        }
};

// accept input from command line switches (algo, seed, n) file? 
params* handleSwitches(int argc, char** argv) {
    params *p = (params*) malloc(sizeof(params));
    p->algo = XORSHIFT;
    p->seed = 1;
    p->n = 16;
    const char* xorshift_str = "xorshift";
    const char* splitmix_str = "splitmix";
    int option;
    while ((option = getopt(argc, argv, "df:a:s:n:")) != -1) {
        switch (option) {
            case 'd':
                debug = 1;
                break;
            case 'f':
                isOutFile = 1;
                outFile = optarg;
                break;
            case 'a':
                if (strcmp(optarg, xorshift_str) == 0) {
                    p->algo = XORSHIFT;
                } else if (strcmp(optarg, splitmix_str) == 0) {
                    p->algo = SPLITMIX;
                }
                break;
            case 's':
                p->seed = (uint64_t) atoi(optarg);
                break;
            case 'n':
                p->n = atoi(optarg);
                break;
            default:
                fprintf(stderr, "Usage: %s [-d] [-f outputFileName] [-a algorithm] [-s seed] [-n numValues]", argv[0]);
                exit(EXIT_FAILURE);
        }
    }
    return p;
}

// generate output file of n random scalars [0, 1) from PRNGStream Object
void buildToOutFile(PRNGStream* r, int n) {
    PRNGStream rng = *r;
    std::ofstream output;
    if (debug) std::cout << "Opening output file '" << outFile << "'...\n";
    output.open(outFile);
    for (int i = 0; i < n; i++) {
        double x = rng.next();
        if (debug) std::cout << "Piping to file'" << outFile << "' value: " << x << "\n";
        output << rng.next() << ' ';
    }
    if (debug) std::cout << "Closing output file '" << outFile << "'...\n";
    output.close();
    if (debug) std::cout << "Output file '" << outFile << "' closed successfully\n";
}

// generate output of n random scalars [0, 1) from PRNGStream Object
void buildToStdOut(PRNGStream* r, int n) {
    PRNGStream rng = *r;
    for (int i = 0; i < n; i++) {
        if(debug) { std::cout << "State = " << rng.getState() << ", Scalar = " << rng.next() << '\n'; }
        else { std::cout << rng.next() << '\n'; }
    }
}

int main(int argc, char** argv) {
    // fill parameters from switches p = { int algo, uint64_t seed, int n }
    params* p = handleSwitches(argc, argv);
    PRNGStream rng = PRNGStream(p->seed, p->algo);

    if (isOutFile) { buildToOutFile(&rng, p->n); } 
    else { buildToStdOut(&rng, p->n); }

    free(p);
    return 0;
}
