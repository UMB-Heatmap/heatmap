# 2D HEATMAP VISUALIZATION:
#   generates N x M heatmap of random numbers

# Visuals are called from main.py with initial parameters algorithm and seed:
#   python3 2d.py (algorithm) (seed)

# Any additional visualization-specific parameters should be acquired 
# within said visualization script by prompting the user via standard input

# 2D Visualization requires 3 additional inputs:
#   number_of_rows, number_of_columns, color_map

from subprocess import run
import numpy as np
import matplotlib.pylab as plt
import sys

# main.py validates user input so we can assume proper CLI input
ALGORITHM = sys.argv[1]
START_SEED = int(sys.argv[2])
SEED_INCREMENT = 1 # default value

# Color Map Options (directly from MatPlotLib)
# https://matplotlib.org/stable/gallery/color/colormap_reference.html
COLOR_MAPS = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'binary', 
            'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper']

# validates int from standard input
def getIntFromInput(message):
    while True: 
        try:
            x = int(input(message))
            return x
        except ValueError:
            print("Invalid Input -- Must be Integer")

# validates color map string from standard input
def getColorMap():
    cmap = input("Color Map: ")
    while (cmap not in COLOR_MAPS):
        print("\nInvalid Color Map -- Select From:")
        print("-----------------------------------")
        for cmap in COLOR_MAPS:
            print(cmap)
        print()
        cmap = input("Color Map: ")
    return cmap
            
# STEP 1: Acquire and Validate visualization-specific inputs
numRows = getIntFromInput("Number of Rows: ")
numCols = getIntFromInput("Number of Columns: ")
colorMap = getColorMap()

# STEP 2: Generate data for visualization via prng.cpp calls
#   to get NUM_VALUES random doubles in range [0, 1) using ALGORITHM and SEED:
#
#       ./prng -f data/OUTPUT_FILENAME.txt -a ALGORITHM -s SEED -n NUM_VALUES
#   
#   then read random numbers from txt file data/OUTPUT_FILENAME.txt 
#
#   NOTE: output txt files are meant as intermediate data storage so naming is arbitrary
data = []
for n in range(numRows):
    filePath = "data/output.txt"
    cmd = './prng -f ' + filePath + ' -a ' + str(ALGORITHM) + ' -s ' + str(START_SEED + n * SEED_INCREMENT) + ' -n ' + str(numCols)
    run(cmd, shell=True)
    row = list(np.genfromtxt(filePath))
    data.append(row)

# STEP 3: Generate visualization
plt.imshow(data, cmap=colorMap)
plt.title(str(numRows) + "x" + str(numCols) + " Heat Map from " + ALGORITHM.upper())
plt.colorbar()

# STEP 4: Save visualization in heatmaps folder with appropriate name
heatmapPath = 'heatmaps/' + str(ALGORITHM) + '_' + str(numRows) + 'x' + str(numCols) + '_2d_heatmap.svg'
plt.savefig(heatmapPath)

# STEP 5: Open visualization 
cmd = 'open ' + heatmapPath
run(cmd, shell=True)

