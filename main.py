# MAIN DRIVER FOR HEATMAP PROJECT:
#   1. validates algorithm and visualization options from command-line arguments
#   2. calls corresponding visualization script with desired algorithm and seed
#
# EXAMPLE USAGE:
#
#   python3 main.py (algorithm) (visual) [seed]
#
# requires algorithm and visual, seed is optional and will default to DEFAULT_SEED

import subprocess
from src import visuals_utils as vis

# install dependencies via pip WORK IN PROGRESS
# subprocess.run([sys.executable, '-m', 'pip3', 'install', '-q', '-r', 'requirements.txt'], shell=True, check=True)
# subprocess.run('python3 -m pip install -q -r requirements.txt', shell=True, check=True)

# Run external script for visualization
vis.makeIfNeeded()
algorithm, visual, seed = vis.handleCLI()
cmd = 'python3 ' + 'src/' + visual + '.py ' + algorithm + ' ' + str(seed)
subprocess.run(cmd, shell=True)