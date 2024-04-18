EXAMPLE USAGE:

    python3 main.py (ALGORITHM) (VISUAL) [SEED]

    - should now run 'Make clean' and 'Make' to rebuild C++ automatically if it needs to

Where:

    ALGORITHM = 'lehmer' | 'splitmix'| 'xorshift' | 'lcg' | ...
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
        - IDEA: include max_int attribute for each algorithm to scale with
                instead of always using max_uint64_t
        - may just need to scale

    LCG also giving values ~ 1e-11
        - IDEA: implement/adjust max_int attribute

    allow python main file to accept additional (optional) arguments for use with the -O flag.
        - IDEA: can also use default algorithm to generate additional values if needed / unspecified

    Lagged Fibonacci arguments:

        ./prng [other arguments] -a lfg -O (operator_char,j_int,k_int)

        operator_char can be '*', '+', '-', or '^'
            - right now only '*' seems to make sense, but other ones can show the flawed nature of the algorithm
            
        In the parenthesis are comma separated values.

        Ex:
            ./prng -d -a lfg -s 1 -n 10 -O *,3,9
