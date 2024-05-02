EXAMPLE USAGE:

    python3 main.py (ALGORITHM) (VISUAL) [SEED]

Where:

    ALGORITHM = 'lehmer' | 'splitmix'| 'xorshift' | 'lcg' | 'middle_square' | 'lfg' | 'rule30' | 'bbs' 
    VISUAL = '2d' | 'distribution' | 'frequency' | '3d_scatter' | '3d_walk' | '3d' | 'shadedrelief' | 'seed_eval'
    SEED = [<optional> Integer]

VISUALS :: result

    2d           :: NxM Heatmap of Random Values [0, 1) with color mapped to each value

    distribution :: NxM Heatmap animated .gif of Distributions of (X) Random Values [0, N)
                    per M iterations with color mapped to the distribution of each value

    frequency    :: NxN Heatmap of Frequency of random number with color mapped to random 
                    2D point selection frequency (darker = more frequently selected)

    3d_scatter   :: Interactive 3D Scatter Plot with N Random Points and multiple 
                    color mapping options.

    3d_walk      :: Interactive 3D plot of N points generated from a step of +- X in each 
                    (x, y, z) direction connected by lines to visualize a 3D random walk. 
                    Also has functionality to generate .gif animation of random walk.
    
    3d           :: 3D heatmap of N points generated from a starting seed or a seed 
                    aquired from user input. N number of points is aquired from user input 
                    User has the option of Interpolation which is preformed to generate the nessesary
                    points between each randomly generated point, creating a smoother map.
                    The smoothness can be controlled by the number of interpolation points 
                    aquired from user input. Best result/preformance is around 100 interP.

    shadedrelief :: Generates a .gif animation of a random 2D heatmap with a variable 
                    light source. 

    seed_eval    :: NxM Heatmap of M values from N different seeds in a user-specified 
                    range with options for color mapping. 

TO DOWNLOAD NECESSARY PACKAGES:

    pip install -r requirements.txt


TODO:
    LCG and Lehmer not scaling properly:
        - set this->maxValue in algorithm header constructor

    Rule30 only giving 1's (at least with default seed)

    Maybe create a Default Seed Manager in python front end for Rule30, Middle_square

    GENERAL TESTING for bugs between all algos and visuals
    
NOTES:

    - OS-dependent command:
        $ open
        Variations:
            Mac ('Darwin'): open 'path/to/file.svg'
            Linux: xdg-open 'path/to/file.gif'
            Windows: 'path/to/file.gif'

    - Moved Dependencies list to requirements.txt

    - main.py will run 'make clean' and 'make' to rebuild C++ automatically if u do not have working ./prng file

    ***IF YOU ARE HAVING TROUBLE WITH PACKAGES:
        install conda from (https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
        then run:

            conda create -n [ENV_NAME] python=3.8
            conda install matplotlib
            conda install numpy
            conda install scipy

    ***to create virtual environment with all necessary packages for heatmap visuals

    For Implementing additional Algorithms:
        1. copy include/template.h and implement peekNext()
        2. update include/master_header.h HEADER, INDEX, and COMMAND LINE NAME
        3. update src/visuals_utils.py ALGORITHM list
        if algorithm requires additional arguments (-O flag):
            1. update src/visuals_utils.py HAS_EXTRA_ARGS list 
            2. update src/visuals_utils.py getAlgoArgs() with elif case for algorithm
            3. update src/visuals_utils.py nRandomScalars() with elif case for algorithm

    For Implementing additional Visualizations:
        1. write VISUALIZATION_NAME.py in src folder 
        **(import visual_utils as vis)
        **(see src/2d.py for example and exaplanation)
        **(see src/visuals_utils.py for common functions and shared values)
        2. update src/visuals_utils.py VISUALS list
        3. IMPORTANT: use ALGO_ARGS = vis.getAlgoArgs(ALGORITHM) and use vis.nRandomScalars() to get data (see examples)
        4. add any python dependencies to requirements.txt

    Lagged Fibonacci arguments Example:
        ./prng [other arguments] -a lfg -O "operator_char,j_int,k_int"
        operator_char can be '*', '+', '-', or '^'
            - right now only '*' seems to make sense
        In the quotes are comma separated values.
        Ex:
            ./prng -d -a lfg -s 1 -n 10 -O "*,3,9"

    Blum Blum Shub arguments:
        ./prng [other arguments] -a bbs -O p,q
        p and q must be Blum Primes, prime numbers that are congruent to 3(mod 4)
        Ex. 3,7,11,19,23,etc
        Ex: ./prng -d -a bbs -s 3 -n 10 -O "11,23"
