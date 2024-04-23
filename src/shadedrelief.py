# SHADED RELIEF HEATMAP VISUALIZATION
# Creates an animation with a light source that moves over time

from subprocess import run
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
from matplotlib.animation import FuncAnimation
from matplotlib.cm import get_cmap
import sys
import visuals_utils as vis

ALGORITHM = sys.argv[1]
ALGO_ARGS = vis.getAlgoArgs(ALGORITHM)
START_SEED = int(sys.argv[2])
SEED_INCREMENT = 12345 #default 
fig, ax = plt.subplots()
# GET "n" to create nxn array
numRowsCols = vis.getIntFromInput("Number of rows/cols: ")
# Get color map - get_cmap is necessary because it's a string by default and can't be used as an object
colorMap = vis.getColorMap()
#colorMap = get_cmap(colorMap)


# GENERATE data 
array = vis.nRandomScalars(ALGORITHM, START_SEED, numRowsCols*numRowsCols, ALGO_ARGS)
array = np.array(array)

# creates a 2d array
world = array.reshape(numRowsCols, numRowsCols)

# function to update plot for each frame
def update(frame):
    # clear current plot
    ax.clear()
    # increment by 5 degrees for each frame
    altdeg = frame * 5
    if altdeg > 360:
        altdeg = -360 # keep angle between 0 and 360

        # update light source with new altitude angle
    ls = LightSource(azdeg= 0 , altdeg=altdeg)
    # shade the world array with new light source
    rgb = ls.shade(world, plt.colormaps.get_cmap(colorMap))
    # plot shaded world array
    ax.imshow(rgb)
    # shows current angle as a title 
    ax.set_title(f'Altitude Angle: {altdeg} degrees')
    # 72 frames to fully rotate 360 degs
ani = FuncAnimation(fig, update, frames = range(72) ,interval = 200)

# ls and rgb redefined out of the animation function
# for the sake of generating a static image
ls = LightSource(azdeg= 0 , altdeg = 0)
rgb = ls.shade(world, plt.colormaps.get_cmap(colorMap))
# does the animation
plt.show() 
# gets the static image
plt.imshow(rgb, cmap =colorMap )

# sets the heatmap path
heatmapPath = 'heatmaps/' + str(ALGORITHM) + '_' + str(numRowsCols) + 'x' + str(numRowsCols) + '_shadedrelief_heatmap.svg'
plt.savefig(heatmapPath)

cmd = 'open ' + heatmapPath
run(cmd, shell=True)

