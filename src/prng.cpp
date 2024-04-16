#include <iostream>
#include <fstream>
#include <string>
#include <stdint.h>
#include <unistd.h>
#include <string.h>
#include <limits>
#include "../include/master_header.h"

class AlgorithmRunner {
private: 
    int algo;
    int n;
    uint64_t seed;
    bool debug;
    bool isOutFile;
    std::string outFile;
    Algorithm *rng;
    std::deque<int> algOpt_int;
    std::deque<std::string> algOpt_string;
public:
    AlgorithmRunner(params p) {
        this->algo = p.algo;
        this->n = p.n;
        this->seed = p.seed;
        this->debug = p.debug;
        this->isOutFile = p.isOutFile;
        this->outFile = p.outFile;
        this->rng = nullptr;
        this->algOpt_int = p.algOpts_int;
        this->algOpt_string = p.algOpts_string;
        
        this->setAlgorithm(p.algo);

        this->rng->setDebug(this->debug);
    };
    ~AlgorithmRunner() {
        delete this->rng;
    };

    float next() {
        this->rng->next();
        float randScalar = ((float) this->rng->getState() / (float) this->rng->maxValue); 
        return randScalar;
    }

    void setAlgorithm(int algorithm) {
        if (algorithm == this->algo && this->rng != nullptr) {
            return;
        }
        delete this->rng;
        this->rng = getAlgorithm(algorithm, this->seed, this->algOpt_int, this->algOpt_string);
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

void readMultiple(char *arg, std::deque<int> *deque_int, std::deque<std::string> *deque_string) {
    std::stringstream ss(arg);
    std::string token;
    while (std::getline(ss, token, ',')) {
        if (token.length() == 1 && std::isdigit(token[0])) {
            deque_int->push_back(std::stoi(token));
        } else {
            deque_string->push_back(token);
        }
        arg++;
    }
}

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
    while ((option = getopt(argc, argv, "df:a:s:n:O:")) != -1) {
        switch (option) {
            case 'd':
                p.debug = true;
                break;
            case 'f':
                p.isOutFile = true;
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
            case 'O':
                readMultiple(optarg, &p.algOpts_int, &p.algOpts_string);
                break;
            default:
                fprintf(stderr, "Usage: %s [-d] [-f outputFileName] [-a algorithm] [-s seed] [-n numValues] [-O algorithm options]\n", argv[0]);
                exit(EXIT_FAILURE);
        }
    }
    return p;
}

int main(int argc, char** argv) {
    // fill parameters from switches p = { int algo, uint64_t seed, int n }
    try {
        params p = handleSwitches(argc, argv);
        AlgorithmRunner *runner = new AlgorithmRunner(p);
        if (p.isOutFile) {
            runner->buildToOutFile(); 
        } 
        else {
            runner->buildToStdOut(); 
        }
    } catch (const std::runtime_error &err) {
        std::cerr << err.what() << std::endl;
    }
    
    return 0;
}
