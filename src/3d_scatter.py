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
from PIL import Image
import os

debug = False

# main.py validates user input so we can assume proper CLI input
ALGORITHM = sys.argv[1]
ALGO_ARGS = vis.getAlgoArgs(ALGORITHM)
START_SEED = int(sys.argv[2])
SEED_INCREMENT = 12345 # default value
MAX_FRAMES = 250 # limit maximum number of .gif frames (250 frames will take about 1-2 minutes to generate)
N = 100 # default scalar for random values

# STEP 1: Acquire and Validate visualization-specific inputs
MAX_VALUES = vis.getIntFromInput("Maximum Number of Random Points: ")
colorMap = vis.getColorMap()
colorMode = vis.getColorMode()
genGif = vis.getBoolFromInput("Would you like to generate a .gif? (Y/N): ")
if (genGif): isLoop = vis.getBoolFromInput("GIF Looping? (Y/N): ")

# create 3d_scatter subfolder if not exists
if not os.path.exists('heatmaps/3d_scatter'):
    os.makedirs('heatmaps/3d_scatter')

# STEP 2: Generate data for visualization via prng.cpp calls
data = []
if (colorMode == 1): numAxis = 4 
else: numAxis = 3
all_data = vis.nRandomScalars(ALGORITHM, START_SEED, MAX_VALUES*numAxis, ALGO_ARGS)
for i in range(numAxis):
    axis = all_data[(i*MAX_VALUES):((i+1)*MAX_VALUES)]
    for i in range(MAX_VALUES): axis[i] = axis[i] * N # scale values
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
    valmax=50,
    valinit=1,
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

if (genGif):
    # display progress
    
    # generate .gif frames
    plt.close()
    framePaths = []
    frames = []
    numFrames = min(MAX_VALUES, MAX_FRAMES)
    if (numFrames == MAX_VALUES): valuesPerFrame = 1
    else: valuesPerFrame = MAX_VALUES // MAX_FRAMES
    for n in range(numFrames):
        if (not debug): print("Generating GIF... " + str(round(100 * (n / numFrames))) + "%")
        i = n*valuesPerFrame
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        ax.scatter(
            x[0:i], 
            y[0:i], 
            z[0:i], 
            c=color[0:i], 
            marker='o', 
            cmap=colorMap, 
            alpha=1
        )
        scatterPath = 'heatmaps/3d_scatter/' + str(ALGORITHM) + '_3d_scatter_frame_' + str(i) + '.png'
        framePaths.append(scatterPath)
        plt.savefig(scatterPath)
        plt.close()

        # clear progress for next update
        if (not debug): os.system('clear')

    # STEP 5: Open .png frames to generate .gif from numIterations 
    for png_path in framePaths:
        # convert to .png and open
        img = Image.open(png_path)
        frames.append(img)

    # generate .gif
    gifPath = 'heatmaps/' + str(ALGORITHM) + '3d_scatter_' + str(MAX_VALUES) + '.gif'
    frames[0].save(gifPath, save_all=True, append_images=frames[1:], loop=(not isLoop)) # duration=gifDuration

    # clean up pngs
    for file in os.listdir('heatmaps/3d_scatter'):
        if file.endswith('.png'):
            os.remove('heatmaps/3d_scatter/' + file)

    # open .gif
    # cmd = 'open ' + gifPath
    # run(cmd, shell=True)
    vis.openVisual(gifPath)

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


