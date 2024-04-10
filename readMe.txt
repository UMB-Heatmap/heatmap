EXAMPLE USAGE:

    Make clean
    Make
    python3 main.py (ALGORITHM) (VISUAL) [SEED]

Where:

    ALGORITHM = 'lehmer' | 'splitmix'| 'xorshift' | ...
    VISUAL = '2d' | distribution | ...
    SEED = [<optional> Integer]

For Implementing additional Algorithms:
    1. copy include/template.h and implement peekNext()
    2. update include/master_header.h HEADER, INDEX, and COMMAND LINE NAME
    3. update src/main.py ALGORITHM list

For Implementing additional Visualizations:
    1. write VISUALIZATION_NAME.py in src folder 
      **(see src/2d.py for example and exaplanation)
    2. update src/main.py VISUALS list

TODO:
    xorshift always giving first value ~ 0 
        - IDEA: might just need to advance seed once upon initilization

    lehmer seems to only be giving values [0, 1e-10) 
        - IDEA: check algorithm implementation for correctness 
        - may just need to scale

