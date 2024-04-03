#include <iostream>
#include <fstream>
#include <string>
#include <stdint.h>
#include <unistd.h>
#include <string.h>

#include "../master_header.h"

class AlgorithmRunner {
private: 
    int algo;
    int n;
    uint64_t seed;
    bool debug;
    int isOutFile;
    std::string outFile;
    Algorithm *rng;
public:
    AlgorithmRunner(params p) {
        this->algo = p.algo;
        this->n = p.n;
        this->seed = p.seed;
        this->debug = p.debug;
        this->isOutFile = p.isOutFile;
        this->outFile = p.outFile;
        this->rng = nullptr;
        this->setAlgorithm(p.algo);
    };
    ~AlgorithmRunner() {
        delete this->rng;
    };

    float next() {
        this->rng->next();
        float randScalar = ((float) this->rng->getState() / (float) std::numeric_limits<uint64_t>::max()); 
        return randScalar;
    }

    void setAlgorithm(int algorithm) {
        if (algorithm == this->algo && this->rng != nullptr) {
            return;
        }
        delete this->rng;
        this->rng = getAlgorithm(algorithm, this->seed);
    }

    // generate output file of n random scalars [0, 1) from PRNGStream Object
    void buildToOutFile() {
        std::ofstream output;
        if (this->debug) std::cout << "Opening output file '" << this->outFile << "'...\n";
        output.open(this->outFile);
        for (int i = 0; i < this->n; i++) {
            double x = this->next();
            if (this->debug) std::cout << "Piping to file'" << this->outFile << "' value: " << x << "\n";
            output << x << ' ';
        }
        if (this->debug) std::cout << "Closing output file '" << this->outFile << "'...\n";
        output.close();
        if (this->debug) std::cout << "Output file '" << this->outFile << "' closed successfully\n";
    }

    // generate output of n random scalars [0, 1) from PRNGStream Object
    void buildToStdOut() {
        for (int i = 0; i < this->n; i++) {
            double x = this->next();
            if(this->debug) { std::cout << "State = " << this->rng->getState() << ", Scalar = " << x << '\n'; }
            else { std::cout << x << '\n'; }
        }
    }
};

// accept input from command line switches (algo, seed, n) file? 
params handleSwitches(int argc, char** argv) {
    params p;
    
    // Set default values
    p.algo = XORSHIFT;
    p.seed = 1;
    p.n = 16;
    p.debug = false;
    p.isOutFile = false;
    p.outFile = "test.txt";

    int option;
    while ((option = getopt(argc, argv, "df:a:s:n:")) != -1) {
        switch (option) {
            case 'd':
                p.debug = true;
                break;
            case 'f':
                p.isOutFile = false;
                p.outFile = optarg;
                break;
            case 'a':
                p.algo = getAlgorithmNum(optarg);
                break;
            case 's':
                p.seed = (uint64_t) atoi(optarg);
                break;
            case 'n':
                p.n = atoi(optarg);
                break;
            default:
                fprintf(stderr, "Usage: %s [-d] [-f outputFileName] [-a algorithm] [-s seed] [-n numValues]", argv[0]);
                exit(EXIT_FAILURE);
        }
    }

    return p;
}

int main(int argc, char** argv) {
    // fill parameters from switches p = { int algo, uint64_t seed, int n }
    params p = handleSwitches(argc, argv);
    AlgorithmRunner *runner = new AlgorithmRunner(p);

    if (p.isOutFile) {
        runner->buildToOutFile(); 
    } 
    else {
        runner->buildToStdOut(); 
    }
    return 0;
}
