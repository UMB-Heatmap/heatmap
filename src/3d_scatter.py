# Interactive 3D scatter plot of randomly generated 3D points
#
# Visuals are called from main.py with initial parameters algorithm and seed:
#   python3 3d_scatter.py (algorithm) (seed)
#
# additional parameters (from standard input):
#   maximum number of points
#   color map
#   color mode
#
# sliders (for interactive 3D plot):
#    number of points shown
#    size of points
# 
# can use native matplotlib zoom to explore distribution of random points

from pylab import *

from subprocess import run
import numpy as np
import matplotlib.pylab as plt
import sys
import visuals_utils as vis

# main.py validates user input so we can assume proper CLI input
ALGORITHM = sys.argv[1]
START_SEED = int(sys.argv[2])
SEED_INCREMENT = 12345 # default value

N = 100 # default scalar for random values



# STEP 1: Acquire and Validate visualization-specific inputs
MAX_VALUES = vis.getIntFromInput("Maximum Number of Random Points: ")
colorMap = vis.getColorMap()
colorMode = vis.getColorMode()

# STEP 2: Generate data for visualization via prng.cpp calls
data = []
if (colorMode == 1): numAxis = 4 
else: numAxis = 3
for i in range(numAxis):
    filePath = "data/output.txt"
    cmd = './prng -f ' + filePath + ' -a ' + str(ALGORITHM) + ' -s ' + str(START_SEED + i * SEED_INCREMENT) + ' -n ' + str(MAX_VALUES)
    run(cmd, shell=True)
    nums = np.genfromtxt(filePath)
    if (nums.size == 1): axis = [nums.item()]
    else: axis = list(nums)
    for i in range(MAX_VALUES): # scale values
        axis[i] = axis[i] * N
    data.append(axis) # append axis of numVals values scaled to [0, N)
    
# STEP 3: Generate visualization
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Horizontal slider to control number of points displayed
axNumPoints = fig.add_axes([0.25, 0.1, 0.65, 0.03])
numPoints_slider = Slider(
    ax=axNumPoints,
    label='Random Points',
    valmin=0,
    valmax=MAX_VALUES,
    valinit=round(MAX_VALUES / 10),
)
# Vertical slider to control size of random points
axPointSize = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
pointSize_slider = Slider(
    ax=axPointSize,
    label='Point Size',
    valmin=0.1,
    valmax=20,
    valinit=5,
    orientation='vertical'
)
# update plot when slider value changes
def update(val):
    values = round(numPoints_slider.val)
    ax.cla()
    ax.scatter(
        x[0:values], 
        y[0:values], 
        z[0:values], 
        s=pointSize_slider.val, 
        c=color[0:values], 
        marker='o', 
        cmap=colorMap, 
        alpha=1
    )
# register update function with NumPoints slider
numPoints_slider.on_changed(update)
pointSize_slider.on_changed(update)

# unpack data / colors
x = data[0]
y = data[1]
z = data[2]
if (colorMode == 1): # random
    color = data[3] 
elif (colorMode == 2): # diagonal gradient
    color = [0] * MAX_VALUES
    for i in range(MAX_VALUES):
        color[i] = (x[i] + y[i] + z[i])
elif (colorMode == 3):  # x gradient
    color = x.copy()
elif (colorMode == 4): # y gradient
    color = y.copy()
elif (colorMode == 5): # z gradient
    color = z.copy()

# initialize plot
values = round(numPoints_slider.val)
ax.scatter(
    x[0:values], 
    y[0:values], 
    z[0:values], 
    c=color[0:values], 
    marker='o', 
    cmap=colorMap, 
    alpha=1
)
plt.show()


