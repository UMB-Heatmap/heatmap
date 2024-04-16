EXAMPLE USAGE:

    python3 main.py (ALGORITHM) (VISUAL) [SEED]

    - should now run 'Make clean' and 'Make' to rebuild C++ automatically if it needs to

    If you need to test your algorithm:
        ./prng [-d] [-a YOUR_ALGORITHM] [-s YOUR_SEED] [-n GENERATE_N_NUMBERS] [-O COMMA,SEPARATED,ARGUMENTS]

Where:

    ALGORITHM = 'lehmer' | 'splitmix'| 'xorshift' | ...
    VISUAL = '2d' | distribution | frequency | ...
    SEED = [<optional> Integer]

For Implementing additional Algorithms:
    1. copy include/template.h and implement peekNext()
    2. update include/master_header.h HEADER, INDEX, and COMMAND LINE NAME
    3. update src/main.py ALGORITHM list

For Implementing additional Visualizations:
    1. write VISUALIZATION_NAME.py in src folder 
      **(see src/2d.py for example and exaplanation)
      **(see src/visuals_utils.py for common functions)
    2. update src/main.py VISUALS list

TODO:
    xorshift always giving first value ~ 0 
        - IDEA: might just need to advance seed once upon initilization

    lehmer seems to only be giving values [0, 1e-10) 
        - IDEA: check algorithm implementation for correctness 
        - may just need to scale

    test LCG algorithm with all visuals

    allow python main file to accept additional (optional) arguments for use with the -O flag.
