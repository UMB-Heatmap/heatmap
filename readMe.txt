EXAMPLE USAGE:

    python3 main.py (ALGORITHM) (VISUAL) [SEED]

    - should run 'Make clean' and 'Make' to rebuild C++ automatically if it needs to

Where:

    ALGORITHM = 'lehmer' | 'splitmix'| 'xorshift' | 'lcg' | 'middle_square' | ...
    VISUAL = '2d' | 'distribution' | 'frequency' | '3d_scatter' | '3d_walk' | '3d' | ...
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

Python Dependencies:
    matplotlib
    numpy
    scipy
    ...

*On Mac OS if pip does not work use Brew.

For Implementing additional Algorithms:
    1. copy include/template.h and implement peekNext()
    2. update include/master_header.h HEADER, INDEX, and COMMAND LINE NAME
    3. update src/visuals_utils.py ALGORITHM list
    if algorithm requires additional arguments (-O flag):
        1. upate src/visuals_utils.py HAS_EXTRA_ARGS list 
        2. update src/visuals_utils.py getAlgoArgs() with elif case for algorithm
        3. update src/visuals_utils.py nRandomScalars() with elif case for algorithm

For Implementing additional Visualizations:
    1. write VISUALIZATION_NAME.py in src folder 
      **(see src/2d.py for example and exaplanation)
      **(see src/visuals_utils.py for common functions and shared values)
    2. update src/visuals_utils.py VISUALS list
    3. use ALGO_ARGS = vis.getAlgoArgs(ALGORITHM) and use vis.nRandomScalars() to get data (see examples)

TODO:
    Lehmer, LCG, and middle_square:
        set this->maxValue in algorithm header constructor

    LFG fails with 2-digit j or k values
        **(I added a safeguard to the src/visual_utils.py getAlgoArgs() to only allow i,k = 1-9
           but this can be removed if this was a bug and gets fixed)

    GENERAL TESTING for bugs between all algos and visuals

    DONE: Convert visuals to only use a single call to nRandomScalars() for better preformance
    and more consistent PRNG states without having to use SEED_INCREMENT


**** Otherwise, all algorithms work with all visuals ****
if having errors with gif creation for distribution, 3d_scatter, or 3d_walk, check that you have:
    heatmaps/3d_scatter/
    heatmaps/3d_walk/
    heatmaps/distribution/
subfolders in the heatmaps folder

    Lagged Fibonacci arguments:
        ./prng [other arguments] -a lfg -O "operator_char,j_int,k_int"
        operator_char can be '*', '+', '-', or '^'
            - right now only '*' seems to make sense
        In the quotes are comma separated values.
        Ex:
            ./prng -d -a lfg -s 1 -n 10 -O *,3,9

