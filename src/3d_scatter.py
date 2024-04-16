# WIP
# 3d scatter plot of randomly selected 3d points

from pylab import *

from subprocess import run
import numpy as np
import matplotlib.pylab as plt
import sys
import visuals_utils as vis


# main.py validates user input so we can assume proper CLI input
ALGORITHM = sys.argv[1]
START_SEED = int(sys.argv[2])
SEED_INCREMENT = 1 # default value
            
# STEP 1: Acquire and Validate visualization-specific inputs
N = vis.getIntFromInput("NxNxN Heatmap... Specify N: ")
numVals = vis.getIntFromInput("Number of Random Points: ")
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
for i in range(3):
    for n in range(N):
        filePath = "data/output.txt"
        cmd = './prng -f ' + filePath + ' -a ' + str(ALGORITHM) + ' -s ' + str(START_SEED + n * SEED_INCREMENT) + ' -n ' + str(numVals)
        run(cmd, shell=True)
        nums = np.genfromtxt(filePath)
        axis = []
        if (nums.size == 1):
            axis = [nums.item()]
        else:
            axis = list(nums)
        
        # scale values
        for i in range(len(axis)):
            axis[i] = axis[i] * N
        
        data.append(axis)
    

# STEP 3: Generate visualization
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
ax.scatter(data[0], data[1], data[2])

color_map = cm.ScalarMappable(cmap=cm.Greens_r)
color_map.set_array([data[0] + data[1] + data[2]])

ax.scatter(data[0], data[1], data[2])

ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
plt.title(str(N) + "x" + str(N) + "x" + str(N) + " Heat Map from " + ALGORITHM.upper())

# STEP 4: Save visualization in heatmaps folder with appropriate name
heatmapPath = 'heatmaps/' + str(ALGORITHM) + '_' + str(N) + 'x' + str(N) + 'x' + str(N) + '_3d_heatmap.svg'
# plt.savefig(heatmapPath)
plt.show()

# STEP 5: Open visualization 
# cmd = 'open ' + heatmapPath
# run(cmd, shell=True)