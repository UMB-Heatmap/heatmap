demo c++ -> python pipeline

to run heatmap_demo.py (produces N*N heatmap using selected algorithm and seed):

    python3 heatmap_demo.py (algorithm) (seed) (N)

where algorithm = 'splitmix' | 'xorshift'
seed = integer
N = number of rows / cols 

to run pi_demo.py (produces monte carlo method graphic with pi estimation using selected algorithm and seed):

    python3 pi_demo.py (algorithm) (seed) (N)

where algorithm = 'splitmix' | 'xorshift'
seed = integer
N = number of random points to draw

to build & run prng:

    g++ prng.cpp -o prng
    ./prng -d [-f outFileName] [-a algorithm] [-s seed] [-n numbersToGenerate]

(-d is an optional debug switch to print debug messages to stdout)
