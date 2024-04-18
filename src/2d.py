# 2D HEATMAP VISUALIZATION:
#   generates N x M heatmap of random numbers

# Visuals are called from main.py with initial parameters algorithm and seed:
#   python3 2d.py (algorithm) (seed)

# Any additional visualization-specific parameters should be acquired 
# within said visualization script by prompting the user via standard input

# 2D Visualization requires 3 additional inputs:
#   number_of_rows, number_of_columns, color_map

from subprocess import run
import matplotlib.pylab as plt
import sys
import visuals_utils as vis

# main.py validates user input so we can assume proper CLI input
ALGORITHM = sys.argv[1]
ALGO_ARGS = vis.getAlgoArgs(ALGORITHM)
START_SEED = int(sys.argv[2])
SEED_INCREMENT = vis.DEFAULT_SEED_INCREMENT
            
# STEP 1: Acquire and Validate visualization-specific inputs
numRows = vis.getIntFromInput("Number of Rows: ")
numCols = vis.getIntFromInput("Number of Columns: ")
colorMap = vis.getColorMap()

# STEP 2: Generate data for visualization via ./prng calls (abstracted to vis.nRandomScalars)
data = []
for n in range(numRows):
    row = vis.nRandomScalars(ALGORITHM, (START_SEED + n * SEED_INCREMENT), numCols, ALGO_ARGS)
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

