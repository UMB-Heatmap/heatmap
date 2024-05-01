# MAIN DRIVER FOR HEATMAP PROJECT:
#   1. validates algorithm and visualization options from command-line arguments
#   2. calls corresponding visualization script with desired algorithm and seed
#
# EXAMPLE USAGE:
#
#   python3 main.py (algorithm) (visual) [seed]
#
# requires algorithm and visual, seed is optional and will default to DEFAULT_SEED

from subprocess import run
from src import visuals_utils as vis
from src.py_classes.imports import *

# Run external script for visualization
vis.makeIfNeeded()

IS_SINGLE_LINE = False

# Create objects
accessor = Accessor()

oi = OptionInfo()
accessor['optionInfo'] = oi

clh = CommandLineHandler(accessor, sys.argv, not IS_SINGLE_LINE)
accessor['commandLineHandler'] = clh

vr = VisualizationRunner(accessor, IS_SINGLE_LINE)
accessor['visualizationRunner'] = vr

# start gathering info
algorithm, visual, seed = clh.getCoreArgs()
extra_args = eac.getOptionalArgs(accessor, algorithm)



# algorithm, visual, seed = vis.handleCLI()
cmd = 'python3 ' + 'src/' + visual + '.py ' + algorithm + ' ' + str(seed)
run(cmd, shell=True)