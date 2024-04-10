# MAIN DRIVER FOR HEATMAP PROJECT:
#   1. validates algorithm and visualization options from command-line arguments
#   2. calls corresponding visualization script with desired algorithm and seed
#
# EXAMPLE USAGE:
#
#   python3 main.py (algorithm) (visual) [seed]
#
# requires algorithm and visual, seed is optional and will default to DEFAULT_SEED

from subprocess import run
import sys

# add algorithm options HERE: (must be all lowercase)
ALGORITHMS = ['lehmer', 'splitmix', 'xorshift']

# add visual options HERE: (must be all lowercase and same as python script name)
VISUALS = ['2d', 'distribution', 'frequency'] 

DEFAULT_SEED = 1

def printAlgorithmOptions():
    for algo in ALGORITHMS: 
            print(algo)

def printVisualOptions():
    for vis in VISUALS:
            print(vis)

def printUsageTable():
    print("\nInvalid Arguments -- Usage:")
    print("-------------------------")
    print("python3 main.py (algorithm) (visual) [seed : Int]\n")
    print("PRNG Algorithm Options:  ")
    print("-------------------------")
    printAlgorithmOptions()
    print("\nVisualization Options: ")
    print("-------------------------")
    printVisualOptions()
    print()

def getAlgorithm():
    algorithm = sys.argv[1].lower()
    if (algorithm not in ALGORITHMS):
        print("Invalid Algorithm -- Select From: ")
        print("----------------------------------")
        printAlgorithmOptions()
        sys.exit()
    return algorithm

def getVisual():
    visual = sys.argv[2].lower()
    if (visual not in VISUALS):
        print("Invalid Visualization -- Select From: ")
        print("--------------------------------------")
        printVisualOptions()
        sys.exit()
    return visual

def getSeed():
    try:
        seed = int(sys.argv[3])
    except ValueError:
        print("Invalid Seed -- Must be Integer")
        sys.exit()
    return seed

# CLI Input with Error Handling and Usage Messages
def handleCLI():
    seed = DEFAULT_SEED
    num_args = len(sys.argv)

    if (num_args == 3 or num_args == 4):
        algorithm = getAlgorithm()
        visual = getVisual()
        if (num_args == 4):
            seed = getSeed()

        return algorithm, visual, seed

    else: 
        printUsageTable()
        sys.exit()

# Run external script for visualization
algorithm, visual, seed = handleCLI()
cmd = 'python3 ' + 'src/' + visual + '.py ' + algorithm + ' ' + str(seed)
run(cmd, shell=True)



