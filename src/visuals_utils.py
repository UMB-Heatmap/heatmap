import numpy as np
from subprocess import run
import sys

def validateInt(value):
        result = True
        try:
            value = int(value)
        except ValueError:
            result = False
        return result

OPTIONS = {
    'algorithms'        : ['lehmer', 'splitmix', 'xorshift', 'lcg', 'middle_square', 'rule30', 'lfg', 'bbs', 'four'],
    'visualizations'    : ['2d', 'distribution', 'frequency', '3d_scatter', '3d_walk', '3d', 'shadedrelief', 'seed_eval'],
    'has_extra_args'    : ['lfg', 'bbs'],
    # Color Map Options (directly from MatPlotLib)
    # https://matplotlib.org/stable/gallery/color/colormap_reference.html
    'color_maps'        : ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink', 'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper'],
    'color_mode_names'  : ['random', 'diagonal gradient', 'x gradient', 'y gradient', 'z gradient'],
    # range(1, LENGTH_OF_color_mode_names + 1)
    'color_modes'       : range(1, 5 + 1),
    'default_seed'      : 12345,
    'default_seed_increment' : 12345,
    'seed'              : validateInt,
}

callbacks = {
    'bbs' : lambda x : x,
    'lfg' : lambda y : y,
}

option_order = ['algorithms', 'visualizations', 'seed']



DEFAULT_SEED = 12345
DEFAULT_SEED_INCREMENT = 12345

# add algorithm options HERE: (must be all lowercase)
ALGORITHMS = ['lehmer', 'splitmix', 'xorshift', 'lcg', 'middle_square', 'rule30', 'lfg', 'bbs', 'four']
HAS_EXTRA_ARGS = ['lfg', 'bbs']

# add visual options HERE: (must be all lowercase and same as python script name)
VISUALS = ['2d', 'distribution', 'frequency', '3d_scatter', '3d_walk', '3d', 'shadedrelief', 'seed_eval'] 


# rebuilds prng.cpp objects via makefile if necessary
def makeIfNeeded():
    try:
        run('./prng -f data/output.txt', shell=True, check=True)
        return
    except:
        print('Rebuilding ./prng ...')
        run('Make clean', shell=True)
        run('Make', shell=True)
        return

# Color Map Options (directly from MatPlotLib)
# https://matplotlib.org/stable/gallery/color/colormap_reference.html
COLOR_MAPS = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'binary', 
            'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper']

# display color map options
def printColorMapOptions():
    print("\nColor Map Options -- Select From:")
    for cmap in COLOR_MAPS:
        print("\t" + cmap)
    print()

# validates color map string from standard input
def getColorMap():
    printColorMapOptions()
    cmap = input("Color Map: ")
    while (cmap not in COLOR_MAPS):
        print("\nInvalid Color Map -- Select From:")
        for cmap in COLOR_MAPS:
            print("\t" + cmap)
        print()
        cmap = input("Color Map: ")
    return cmap

COLOR_MODES_NAMES = ['random', 'diagonal gradient', 'x gradient', 'y gradient', 'z gradient']
COLOR_MODES = range(1, len(COLOR_MODES_NAMES) + 1)

# display color mode options
def printColorModeOptions():
    print("\nColor Modes -- Select From:")
    for i in COLOR_MODES:
        print("\t" + str(i) + ": " + COLOR_MODES_NAMES[i-1])
    print()

# validates color mode option int from standard input
def getColorMode():
    printColorModeOptions()
    colorMode = getIntFromInput("Color Mode: ")
    while (colorMode not in COLOR_MODES):
        colorMode = getIntFromInput("Invalid Input -- Select From:\n\t1: random\n\t2: diagonal gradient\n\t3: x gradient\n\t4: y gradient\n\t5: z gradient\n\nColor Mode: ")
    return colorMode

# validates int from standard input
def getIntFromInput(message):
    while True: 
        try:
            x = int(input(message))
            if (x >= 1):
                return x
            else:
                print("Invalid Input -- Must be >= 1")
        except ValueError:
            print("Invalid Input -- Must be Integer")

# validates yes/no (boolean) input from standard input
def getBoolFromInput(message):
    while True:
        answer = input(message).lower()
        if (answer == 'y' or answer == 'yes'):
            return True
        elif (answer == 'n' or answer == 'no'):
            return False
        else:
            print("Invalid Input -- Must be Yes/No or Y/N")

# validates positive float input from standard input
def getPosFloatFromInput(message):
    while True: 
        try:
            x = float(input(message))
            if (x > 0.0):
                return x
            else:
                print("Invalid Input -- Must be > 0.0")
        except ValueError:
            print("Invalid Input -- Must be > 0.0")

# gets / sanitizes extra arguments for algorithms that require them
def getAlgoArgs(algo):
    if algo not in HAS_EXTRA_ARGS:
        return []
    # IMPORTANT: add case for each algorithm that requires extra arguments
    elif algo == 'lfg':
        op_char = input("Operator (*, +, -, ^): ")
        while op_char not in ['*', '+', '-', '^']:
            op_char = input("Invalid Input -- Select From Operators (*, +, -, ^): ")
        j = -1
        while not (j > 0):
            j = getIntFromInput("J Value: ")
        k = -1
        while not (k > 0 and k != j):
            k = getIntFromInput("K Value: ")
        
        return [op_char, j, k]
    
    elif algo == "bbs":
        p = getIntFromInput("P Value (Blum Prime): ")
        while not isBlumPrime(p):
            p = getIntFromInput("Invalid Input -- P Value must be a Blum Prime: ")
        q = getIntFromInput("Q Value (Blum Prime): ")
        while not isBlumPrime(q):
            q = getIntFromInput("Invalid Input -- Q Value must be a Blum Prime: ")
        return [p, q]

# checks if a number is a Blum Prime
def isBlumPrime(n):
    if n <= 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return n % 4 == 3

# returns list of N scalars [0, 1) from algo and seed or -1 if invalid inputs
def nRandomScalars(algo, seed, numVals, args):
    try: #filter out bad inputs
        s = int(seed)
        n = int(numVals)
        if (s < 0) or (n <= 0): return -1
    except ValueError: return -1
    if (algo.lower() not in ALGORITHMS): return -1

    # get random scalars from ./prng
    filePath = "data/output.txt"

    # IMPORTANT: add case for each algorithm that requires extra arguments
    if algo not in HAS_EXTRA_ARGS:
        cmd = './prng -f ' + filePath + ' -a ' + str(algo.lower()) + ' -s ' + str(s) + ' -n ' + str(n)
    elif algo == 'lfg':
        cmd = './prng -f ' + filePath + ' -a lfg -s ' + str(s) + ' -n ' + str(n) + ' -O \"' + str(args[0]) + ',' + str(args[1]) + ',' + str(args[2]) + '\"'
    elif algo == 'bbs': 
        cmd = './prng -f ' + filePath + ' -a bbs -s ' + str(s) + ' -n ' + str(n) + ' -O \"' + str(args[0]) + ',' + str(args[1]) + '\"'
    run(cmd, shell=True)
    nums = np.genfromtxt(filePath)
    if (nums.size == 1): randoms = [nums.item()]
    else: randoms = list(nums)
    return randoms

