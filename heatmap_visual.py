from subprocess import Popen, PIPE, STDOUT, run, call
import numpy as np
import matplotlib.pylab as plt
import sys

# settings for c++ command flags
ALGORITHM = sys.argv[1] # 'splitmix' # = 'xorshift'
START_SEED = int(sys.argv[2])
N = int(sys.argv[3])

data = []
# create N*N array of data with random numbers
for i in range(N):
    # Get row of random numbers from `./prng` with seed = START_SEED + i
    filePath = "data/output" + str(i) + ".txt"
    cmd = './prng -f ' + filePath + ' -a ' + str(ALGORITHM) + ' -s ' + str(START_SEED + i) + ' -n ' + str(N)
    run(cmd, shell=True)
    row = list(np.genfromtxt(filePath))
    data.append(row)
    
# draw N*N heatmap with random data
plt.imshow(data, cmap='viridis', )
plt.title(str(N) + "x" + str(N) + " Heat Map from " + ALGORITHM.upper())
plt.colorbar()
heatmapPath = 'heatmaps/' + str(ALGORITHM) + '_' + str(N) + 'x' + str(N) + '_heatmap.svg'
plt.savefig(heatmapPath)
cmd = 'open ' + heatmapPath
run(cmd, shell=True)
