# 3D HEATMAP VISUALIZATION WITH INTERPOLATION:
#   generates N number of heatmap of random numbers

# Visuals are called from main.py with initial parameters algorithm and seed:
#   python3 3d.py (algorithm) (seed)

# Any additional visualization-specific parameters should be acquired 
# within said visualization script by prompting the user via standard input

# 3D Visualization requires 3 additional inputs:
#   number_of_points, number_of_interpolation_points, color_map

from subprocess import run
from scipy import interpolate
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
numP = vis.getIntFromInput("Number of Points: ")
interP = vis.getIntFromInput("Number of Interpolation Points (Higher = Smoother): ")
colorMap = vis.getColorMap()


# This only serves to fix an error down the line
colorMap1 = plt.colormaps.get_cmap(colorMap)


# STEP 2: Generate data for visualization via prng.cpp calls
#   to get NUM_VALUES random doubles in range [0, 1) using ALGORITHM and SEED:
#
#       ./prng -f data/OUTPUT_FILENAME.txt -a ALGORITHM -s SEED -n NUM_VALUES
#   
#   then read random numbers from txt file data/OUTPUT_FILENAME.txt 
#
#   NOTE: output txt files are meant as intermediate data storage so naming is arbitrary

data = []
for x in range(numP):
    filePath = "data/output.txt"
    cmd = './prng -f ' + filePath + ' -a ' + str(ALGORITHM) + ' -s ' + str(START_SEED + x * SEED_INCREMENT) + ' -n ' + str(numP)
    run(cmd, shell=True)
    nums = np.genfromtxt(filePath)
    row = []
    if (nums.size == 1):
        row = [nums.item()]
    else:
        row = list(nums)
    data.append(row)


# STEP 3: Generate visualization

# Set up plot
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Original Heatmap without interpolation
X = np.linspace(0, 1, numP)
Y = np.linspace(0, 1, numP)
X, Y = np.meshgrid(X, Y)
Z = np.asarray(data)

# Define new grid for interpolation
newX, newY = np.mgrid[0:1:1j * interP, 0:1:1j * interP]

# Perform interpolation
tck = interpolate.bisplrep(X, Y, Z, s=0)  # Adjust 's' for smoothing level
newZ = interpolate.bisplev(newX[:, 0], newY[0, :], tck)

# Plot interpolated surface
surf = ax.plot_surface(newX, newY, newZ, cmap=colorMap1, antialiased=True)


# STEP 4: Save visualization in heatmaps folder with appropriate name
heatmapPath = 'heatmaps/' + str(ALGORITHM) + '_' + str(START_SEED) + '_3d_heatmap.svg'
plt.savefig(heatmapPath)


# STEP 5: Open visualization
cmd = 'open ' + heatmapPath
run(cmd, shell=True)