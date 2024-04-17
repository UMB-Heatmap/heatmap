# generate gif of random 3d points connected by lines to generate animated random 3d path
# 
# inputs:
#   max_step_size
#   max_step_angle
#   gif looping?
# 
# first frame will generate a random point
#   - each subsequent frame will advance point by some random length step 
#     at some random angle from the previous point

# TODO: 
#   have colors change for individual points / lines
#   implement color modes & color maps

from subprocess import run
import numpy as np
import matplotlib.pyplot as plt
import sys
import visuals_utils as vis
from PIL import Image
import os

debug = False

# main.py validates user input so we can assume proper CLI input
ALGORITHM = sys.argv[1]
START_SEED = int(sys.argv[2])
SEED_INCREMENT = 12345 # default value
N = 100 # default scalar

# clear any warnings
os.system('clear')

# get additional user inputs
steps = vis.getIntFromInput("Number of Steps: ")
max_step_size = vis.getIntFromInput("Maximum Step Size: ")
isLoop = vis.getBoolFromInput("GIF Looping? (Y/N): ")
openPlot = vis.getBoolFromInput("Would you like to Open finished Plot? (Y/N): ")
colorMode =  3 # vis.getColorMode()
# colorMap = vis.getColorMap()

# get random numbers
if colorMode == 1: scale = 7
else: scale = 6
values = steps * scale
filePath = "data/output.txt"
cmd = './prng -f ' + filePath + ' -a ' + str(ALGORITHM) + ' -s ' + str(START_SEED) + ' -n ' + str(values)
run(cmd, shell=True)
nums = np.genfromtxt(filePath)
if (nums.size == 1): randoms = [nums.item()]
else: randoms = list(nums)

# unpack random data
x = []
y = []
z = []
s1 = []
s2 = []
s3 = []
if colorMode == 1: color = []
for i in range(steps):
    if randoms[(i*scale)+3] >= 0.5: s1.append(1)
    else: s1.append(-1)
    if randoms[(i*scale)+4] >= 0.5: s2.append(1)
    else: s2.append(-1)
    if randoms[(i*scale)+5] >= 0.5: s3.append(1)
    else: s3.append(-1)
    if (i == 0):
        x.append(round(randoms[(i*scale)]*N))
        y.append(round(randoms[(i*scale)+1]*N))
        z.append(round(randoms[(i*scale)+2]*N))
    else:
        x.append(x[i-1] + randoms[(i*scale)] * max_step_size * s1[i])
        y.append(y[i-1] + randoms[(i*scale)+1] * max_step_size * s2[i])
        z.append(z[i-1] + randoms[(i*scale)+2] * max_step_size * s3[i])

    if colorMode == 1: color.append(randoms[(i*scale)+6]) # random color mode

# other color mode cases
if (colorMode == 2): # diagonal gradient
    color = [0] * steps
    for i in range(steps):
        color[i] = (x[i] + y[i] + z[i])
elif (colorMode == 3):  # x gradient
    color = x.copy()
elif (colorMode == 4): # y gradient
    color = y.copy()
elif (colorMode == 5): # z gradient
    color = z.copy()

framePaths = []

# generate first point frame
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
ax.plot(round(x[0]*N), round(y[0]*N), round(z[0]*N), marker='o', c='b')
# ax.scatter(round(x[0]*N), round(y[0]*N), round(z[0]*N), c=color[0], cmap=colorMap)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
# plt.show()

# save first plot frame
walkPath = 'heatmaps/3d_walk/' + str(ALGORITHM) + '_' + str(steps) + 'x' + str(max_step_size) + '_3d_walk_frame' + str(0) + '.png'
framePaths.append(walkPath)
plt.savefig(walkPath)
plt.close()

# generate random walk frames
for step in range(1, steps):
    # step: (x, y, z) +- [0, max_step_size)

    # display progress
    if (not debug): print("Generating GIF... " + str(round(100 * (step / steps))) + "%")

    # generate plot frame
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # ax.scatter(x[0:step], y[0:step], z[0:step], c=color[0:step], cmap=colorMap, alpha=0.8)
    ax.plot(x[0:step], y[0:step], z[0:step], marker='o', c='b')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # save plot
    walkPath = 'heatmaps/3d_walk/' + str(ALGORITHM) + '_' + str(steps) + 'x' + str(max_step_size) + '_3d_walk_frame' + str(step) + '.png'
    framePaths.append(walkPath)
    plt.savefig(walkPath)
    if (step != steps-1): # dont clear last frame plot
        plt.close()

    # clear progress for next update
    if (not debug): os.system('clear')

# generate .gif from frames
frames = []
for png_path in framePaths:
    # convert to .png and open
    img = Image.open(png_path)
    frames.append(img)
gifPath = 'heatmaps/' + str(ALGORITHM) + '_' + str(steps) + 'x' + str(max_step_size) + '_3d_walk_frame.gif'
frames[0].save(gifPath, save_all=True, append_images=frames[1:], loop=(not isLoop)) # duration=gifDuration

# clean up pngs
for file in os.listdir('heatmaps/3d_walk'):
    if file.endswith('.png'):
        os.remove('heatmaps/3d_walk/' + file)

# open result
cmd = 'open ' + gifPath
run(cmd, shell=True)
if openPlot: 
    plt.show()
