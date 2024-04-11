# PRNG Integer Distribution Heatmap Visualization:
#   N possible candidates 
#   X Iterations of Z random values [0, N)

# Calculate each row to be % of total (X*Z) in each bucket to show distribution of random ints
# With enough iterations (and a good PRNG algorithm) should balance out to consistent color rows
# Option to normalize distributions for a clearer color gradient between more/less commonly picked integers

# Visuals are called from main.py with initial parameters algorithm and seed:
#   python3 2d.py (algorithm) (seed)

# 2D Visualization requires 4 additional inputs:
#   number_of_candidates : int
#   number_of_iterations : int
#   number_of_values_per_iteration : int
#   color_map : string in COLOR_MAPS
#   is_normalized? : 'y' | 'n'

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
numCandidates = vis.getIntFromInput("Number of Candidates: ")
numIterations = vis.getIntFromInput("Number of Iterations: ")
numValsPerIter = vis.getIntFromInput("Number of Values per Iteration: ")
isNormalized = vis.getBoolFromInput("Normalize Distributions? (Y/N): ")
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
# tracks total number of occurences of each random int in range [0, numCandidates)
rowCount = [0] * numCandidates
# tracks distribution of random ints so far (list elements sum to 1.0)
rowDistribution = [0.0] * numCandidates
total_data_points = 0

for n in range(numIterations):
    # Generate numValsPerIter random values into list output
    filePath = "data/output.txt"
    cmd = './prng -f ' + filePath + ' -a ' + str(ALGORITHM) + ' -s ' + str(START_SEED + n * SEED_INCREMENT) + ' -n ' + str(numValsPerIter)
    run(cmd, shell=True)
    nums = np.genfromtxt(filePath)
    output = []
    if (nums.size == 1):
        output = [nums.item()]
    else:
        output = list(nums)

    for elem in output:
        # Scale random value to integer [0, numCandidates)
        x = int(elem * numCandidates)
        # Increment corresponding element in rowCount for each random value generated
        rowCount[x] += 1
        total_data_points += 1

    # Calculate distribution of random integers for current row
    for i in range(numCandidates):
        rowDistribution[i] = rowCount[i] / float(total_data_points)

    if (isNormalized):
        # Normalize distribution to [0, 1) for clearer color gradient if requested by input 
        min_value = float(np.min(rowDistribution))
        max_value = float(np.max(rowDistribution))
        normalized_row = [(value - min_value) / (max_value - min_value) for value in rowDistribution]
        data.append(normalized_row)
    else:
        # Otherwise use distribution of random ints
        data.append(rowDistribution)

# STEP 3: Generate visualization
plt.imshow(data, cmap=colorMap)
plt.title("Distribution Heat Map from " + ALGORITHM.upper())
isNormStr = ""
if (isNormalized):
    isNormStr = "Normalized "
plt.xlabel(isNormStr + "Distribution of Random Int [0, " + str(numCandidates) + ")")
plt.ylabel("Iterations of " + str(numValsPerIter) + " Random Ints")
plt.colorbar() # TODO: adjust colorbar range for clearer visual effect

# STEP 4: Save visualization in heatmaps folder with appropriate name
heatmapPath = 'heatmaps/' + str(ALGORITHM) + '_' + str(numCandidates) + 'x' + str(numIterations) + 'x' + str(numValsPerIter) + '_distribution_heatmap.svg'
plt.savefig(heatmapPath)

# STEP 5: Open visualization 
cmd = 'open ' + heatmapPath
run(cmd, shell=True)