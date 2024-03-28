from subprocess import Popen, PIPE, STDOUT, call, run
import webbrowser
import matplotlib.pylab as plt
import numpy as np
import sys

# settings for c++ command flags
ALGORITHM = sys.argv[1] # 'splitmix' # = 'xorshift'
SEED = int(sys.argv[2])
N =  int(sys.argv[3])

cmd = './prng -a ' + str(ALGORITHM) + ' -s ' + str(SEED) + ' -n ' + str(N**2)

# Get random numbers from `./prng`
rng = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)

# create N*N array of data with random numbers
# tempOutputFile = open('dummy.txt', "w")
data = np.genfromtxt('dummy.txt')
print(data.shape)
# sys.exit()
b = N // 2
for i in range(N):
    row = []
    for j in range(N):
        if (j > b):
            baseline = 0.4
        else:
            baseline = 0.0
        val = rng.stdout.readline()
        if not val: break

        # rawVal = float(val.strip())
        # heatmapVal = rawVal * 0.1 + baseline
        # ow.append(data[i][j])
        # tempOutputFile.write(str(heatmapVal) + ' ')
   # data.append(row)
    # tempOutputFile.write('\n')
# tempOutputFile.close()

# draw N*N heatmap with random data
plt.imshow(data, cmap='viridis', )
plt.title(str(N) + "x" + str(N) + " Heat Map from " + ALGORITHM.upper())
plt.colorbar()
# plt.show()
plt.savefig('output.svg')
# run(["chrome", "output.svg"])
# call(('open', 'output.svg'), shell=True)

