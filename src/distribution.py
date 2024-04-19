# PRNG Integer Distribution Heatmap Visualization:
#   N possible candidates 
#   X Iterations of Z random values [0, N)
#
# Calculate each row to be % of total (X*Z) in each bucket to show distribution of random ints
# With enough iterations (and a good PRNG algorithm) should balance out to consistent color rows
# Option to normalize distributions for a clearer color gradient between more/less commonly picked integers
#
# Visuals are called from main.py with initial parameters algorithm and seed:
#   python3 2d.py (algorithm) (seed)
#
# 2D Visualization requires 4 additional inputs:
#   number_of_candidates : int
#   number_of_iterations : int
#   number_of_values_per_iteration : int
#   color_map : string in COLOR_MAPS
#   is_looping? : 'y' | 'n'

# TODO: 
#   add sliders for interactive plot
#   optional gif generation

from subprocess import run
import matplotlib.pyplot as plt
import numpy as np
import sys
import visuals_utils as vis
from PIL import Image
import os

debug = False

# main.py validates user input so we can assume proper CLI input
ALGORITHM = sys.argv[1]
ALGO_ARGS = vis.getAlgoArgs(ALGORITHM)
START_SEED = int(sys.argv[2])
SEED_INCREMENT = vis.DEFAULT_SEED_INCREMENT

# clear any warnings
os.system('clear')

# STEP 1: Acquire and Validate visualization-specific inputs
numCandidates = vis.getIntFromInput("Number of Candidates: ")
numIterations = vis.getIntFromInput("Number of Iterations: ")
numValsPerIter = vis.getIntFromInput("Number of Values per Iteration: ")
isNormalized = vis.getBoolFromInput("Normalize Distributions? (Y/N): ")
isLoop = vis.getBoolFromInput("GIF Looping? (Y/N): ")
gifDuration = vis.getPosFloatFromInput("GIF Duration: ")
isScaleColorMap = True # vis.getBoolFromInput("Scale Color Map? (Y/N): ")
colorMap = vis.getColorMap()

# STEP 2: Generate data for visualization via prng.cpp calls (abstracted to vis.nRandomScalars)
data = []
frames = [] # .svg files (1 per Iteration / Row)
framePaths = []
rowCount = [0] * numCandidates # tracks total number of occurences of each random int in range [0, numCandidates)
total_data_points = 0 # tracks distribution of random ints so far (list elements sum to 1.0)
all_data = vis.nRandomScalars(ALGORITHM, (START_SEED), numValsPerIter*numIterations, ALGO_ARGS)
for n in range(numIterations):
    # display progress
    if (not debug): print("Generating GIF... " + str(round(100 * (n / numIterations))) + "%")

    rowDistribution = [0.0] * numCandidates
    # Generate numValsPerIter random values into list output
    output = all_data[(n*numValsPerIter):((n+1)*numValsPerIter)]

    if (debug):
        print("\nPRNG output ----------\n")
        print(output)
        print("-----------------------\n")

    for elem in output:
        # Scale random value to integer [0, numCandidates)
        x = int(elem * numCandidates)
        # Increment corresponding element in rowCount for each random value generated
        rowCount[x] += 1
        total_data_points += 1

    # Calculate distribution of random integers for current row
    for i in range(numCandidates):
        rowDistribution[i] = rowCount[i] / float(total_data_points)

    min_value = float(np.min(rowDistribution))
    max_value = float(np.max(rowDistribution))

    if (debug):
        print("\nRow ----------\n")
        print(rowDistribution)
        print("----------------\n")

    if (isNormalized):
        # Normalize distribution to [0, 1) for clearer color gradient if requested by input 
        normalized_row = [(value - min_value) / (max_value - min_value) for value in rowDistribution]
        data.append(normalized_row)
    else:
        # Otherwise use distribution of random ints
        data.append(rowDistribution)

    if (debug):
        print("\nData " + str(n) + " ---------\n")
        for row in data:
            print(row)
        print("-----------------\n")

    # fill (numIterations - n - 1) rows of 0's to create a complete frame of gif
    frame = data.copy()
    for i in range(numIterations - n - 1):
        frame.append([0.0] * numCandidates)

    if (debug):
        print("\nFrame " + str(n) + " ---------\n")
        for row in frame:
            print(row)
        print("-----------------\n")

    # STEP 3: Generate .svg frame
    if (isScaleColorMap):
        plt.imshow(frame, cmap=colorMap, vmin=min_value, vmax=max_value)
    else:
        plt.imshow(frame, cmap=colorMap, vmin=0.0, vmax=1.0)
    plt.title("Distribution Heat Map from " + ALGORITHM.upper())
    plt.xlabel("Random Int [0, " + str(numCandidates) + ") from " + ALGORITHM.upper())
    plt.ylabel("Iterations of " + str(numValsPerIter) + " Random Ints")
    plt.colorbar() 

    # STEP 4: Save visualization in heatmaps/distribution folder with appropriate name for each frame
    heatmapPath = 'heatmaps/distribution/' + str(ALGORITHM) + '_' + str(numCandidates) + 'x' + str(numIterations) + 'x' + str(numValsPerIter) + '_dist_HM_frame' + str(n) + '.png'
    framePaths.append(heatmapPath)
    plt.savefig(heatmapPath)
    plt.close()

    # clear progress for next update
    if (not debug): os.system('clear')

# STEP 5: Open .png frames to generate .gif from numIterations 
for png_path in framePaths:
    # convert to .png and open
    img = Image.open(png_path)
    frames.append(img)
# generate .gif
gifPath = 'heatmaps/'+ str(ALGORITHM) + '_' + str(numCandidates) + 'x' + str(numIterations) + 'x' + str(numValsPerIter) + '_dist_HM.gif'
frames[0].save(gifPath, save_all=True, append_images=frames[1:], loop=(not isLoop), duration=gifDuration) # duration=gifDuration

# clean up pngs
for file in os.listdir('heatmaps/distribution'):
    if file.endswith('.png'):
        os.remove('heatmaps/distribution/' + file)

cmd = 'open ' + gifPath
run(cmd, shell=True)