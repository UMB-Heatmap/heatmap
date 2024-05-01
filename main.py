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

IS_SINGLE_LINE = False

# Create objects
accessor = Accessor()

oi = OptionInfo()
accessor['optionInfo'] = oi

clh = CommandLineHandler(accessor, sys.argv, not IS_SINGLE_LINE)
accessor['commandLineHandler'] = clh

vh = VisualizationHandler(accessor, IS_SINGLE_LINE)
accessor['visualizationHandler'] = vh

cpp = CppHandler(accessor, not IS_SINGLE_LINE)
accessor['cppHandler'] = cpp

# start gathering info
cpp.makeIfNeeded()

algorithm, visual, seed = clh.getCoreArgs()
extra_args = eac.getOptionalArgs(accessor, algorithm)

params = {
    'algorithm' : algorithm,
    'visualization' : visual,
    'seed' : seed,
    'extra_args' : extra_args
}

accessor.params = params

vh.setup(params)

vh.run()
vh.open()

# algorithm, visual, seed = vis.handleCLI()
# cmd = 'python3 ' + 'src/' + visual + '.py ' + algorithm + ' ' + str(seed)
# run(cmd, shell=True)