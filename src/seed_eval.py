# seed_eval HEATMAP VISUALIZATION:
#   generates N x M heatmap of random numbers with N random seeds

# Visuals are called from main.py with initial parameters algorithm and seed:
#   python3 2d.py (algorithm) (seed)

# Any additional visualization-specific parameters should be acquired 
# within said visualization script by prompting the user via standard input

# 2D Visualization requires 5 additional inputs:
#   number_of_rows, number_of_columns, color_map, minSeed, maxSeed

from subprocess import run
import matplotlib.pylab as plt
import sys
import visuals_utils as vis

# main.py validates user input so we can assume proper CLI input
ALGORITHM = sys.argv[1]
ALGO_ARGS = vis.getAlgoArgs(ALGORITHM)
START_SEED = int(sys.argv[2])

# STEP 1: Acquire and Validate visualization-specific inputs
numRows = vis.getIntFromInput("Number of Rows (Random Seeds): ")
numCols = vis.getIntFromInput("Number of Columns (Values Per Seed): ")
minSeed = vis.getIntFromInput("Minimum seed value: ")
maxSeed = vis.getIntFromInput("Maximum seed value: ")
colorMap = vis.getColorMap()

# STEP 2: Generate data for visualization via ./prng calls (abstracted to vis.nRandomScalars)
seeds = [*range(minSeed, maxSeed+1, int(abs(maxSeed - minSeed) / numRows))]
seeds = seeds[:numRows]
seeds.sort(reverse=True)
data = []
for n in range(numRows):
    row = vis.nRandomScalars(ALGORITHM, seeds[n], numCols, ALGO_ARGS)
    data.append(row)

# STEP 3: Generate visualization
ticks = []
tick_labels = []
plt.ylabel("Seed")
if (numRows > 25): # maximum 25 seed row labels (more than that looks cluttered)
    spacing =  numRows // (25 - 1)
    for x in range(25):
        ticks.append(int(x*spacing))
        tick_labels.append(seeds[int(x*spacing)])
else:
    ticks = [*range(0, numRows)]
    tick_labels = seeds
plt.yticks(ticks, tick_labels)
plt.imshow(data, cmap=colorMap)
plt.title(str(numRows) + "x" + str(numCols) + " Heat Map from " + ALGORITHM.upper())
plt.colorbar()

# STEP 4: Save visualization in heatmaps folder with appropriate name
heatmapPath = 'heatmaps/' + str(ALGORITHM) + '_' + str(numRows) + 'x' + str(numCols) + '_2d_heatmap.svg'
plt.savefig(heatmapPath)

# STEP 5: Open visualization 
cmd = 'open ' + heatmapPath
run(cmd, shell=True)

