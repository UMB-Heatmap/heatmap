# 2D FREQUENCY HEATMAP VISUALIZATION:
#   -Generates NxN heatmap of frequencies of randomly generated numbers
#   
#   -Each randomly generated number maps to some location on the heatmap. Each
#      location is initialized to be the lightest color of the color scheme. When
#      a randomly generated value maps to a particular location, that location's 
#      color is made slightly darker. 
#
#   -Number of randomly generated values = number of locations on heatmap
#
#   -If the distribution of randomly generated numbers was perfectly even, the entire
#      heatmap would be a single color
# 
#   -This map can be used to visualize the distribution of PRNG's
#
# Visuals are called from main.py with initial parameters algorithm and seed:
#   python3 frequency.py (algorithm) (seed)   
#
# Any additional visualization-specific parameters should be acquired 
#   within said visualization script by prompting the user via standard input
#
# 2D Frequency Visualization requires 2 additional inputs:
#   number_of_rows_and_columns, color_map

from subprocess import run
import numpy as np
import matplotlib.pylab as plt
import sys
import visuals_utils as vis

# main.py validates user input so we can assume proper CLI input
ALGORITHM = sys.argv[1]
ALGO_ARGS = vis.getAlgoArgs(ALGORITHM)
START_SEED = int(sys.argv[2])
SEED_INCREMENT = 12345 # default value

# STEP 1: Acquire and Validate visualization-specific inputs
numRowsCols = vis.getIntFromInput("Number of rows/columns: ")
colorMap = vis.getColorMap()

# STEP 2: Generate data for visualization via prng.cpp calls (abstracted to vis.nRandomScalars)
data = []
all_data = vis.nRandomScalars(ALGORITHM, START_SEED, numRowsCols*numRowsCols, ALGO_ARGS)
for n in range(numRowsCols):
    row = all_data[(n*numRowsCols):((n+1)*numRowsCols)]
    data.append(row)

# STEP 3: Convert each entry in the data array to an index of the colors array (same
# size as data). 
# Colors array is initialized to all ones (lightest color in color schemes). When a value
# from data is matched to an index in the colors array, the value at that index is decremented 
# by some value (making the plotted color darker).

colors = [[1 for col in range(numRowsCols)] for row in range(numRowsCols)]
decrementVal = 0.2
for i in data:
    for j in i:
        num = int(j * numRowsCols * numRowsCols)
        colorsRow = int(num / numRowsCols)
        colorsCol = num % numRowsCols
        colors[colorsRow][colorsCol] = colors[colorsRow][colorsCol] - decrementVal 
        # Prevents any value from going below zero 
        if(colors[colorsRow][colorsCol] < 0):
            colors[colorsRow][colorsCol] = 0

# STEP 4: Generate visualization
plt.imshow(colors, cmap=colorMap)
plt.title(str(numRowsCols) + "x" + str(numRowsCols) + " Frequency Heat Map from " + ALGORITHM.upper())
plt.colorbar()

# STEP 5: Save visualization in heatmaps folder with appropriate name
heatmapPath = 'heatmaps/' + str(ALGORITHM) + '_' + str(numRowsCols) + 'x' + str(numRowsCols) + '_frequency_heatmap.svg'
plt.savefig(heatmapPath)

# STEP 6: Open visualization 
# cmd = 'open ' + heatmapPath
# run(cmd, shell=True)
vis.openVisual(heatmapPath)