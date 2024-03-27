from subprocess import Popen, PIPE, STDOUT
import matplotlib.pylab as plt
import sys

# settings for c++ command flags
ALGORITHM = sys.argv[1] # 'splitmix' # = 'xorshift'
SEED = int(sys.argv[2])
N =  int(sys.argv[3])

cmd = './prng -a ' + str(ALGORITHM) + ' -s ' + str(SEED) + ' -n ' + str(N**2)

# Get random numbers from `./prng`
rng = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)

# create N*N array of data with random numbers
data = []
for i in range(N):
    row = []
    for j in range(N):
        val = rng.stdout.readline()
        if not val: break
        row.append(float(val.strip()))
    data.append(row)

# draw N*N heatmap with random data
plt.imshow(data, cmap='viridis', )
plt.title(str(N) + "x" + str(N) + " Heat Map from " + ALGORITHM.upper())
plt.colorbar()
plt.show()

