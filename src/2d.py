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
import visuals_utils as vis

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
            
# STEP 1: Acquire and Validate visualization-specific inputs
numRows = vis.getIntFromInput("Number of Rows: ")
numCols = vis.getIntFromInput("Number of Columns: ")
colorMap = vis.getColorMap()

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
    nums = np.genfromtxt(filePath)
    row = []
    if (nums.size == 1):
        row = [nums.item()]
    else:
        row = list(nums)
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

