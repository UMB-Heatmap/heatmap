from src.py_classes.command_line_handler import CommandLineHandler
from src import visuals_utils as vis_u
import sys

class VisualizationRunner:

    is_single_command = False

    params = {
        'algorithm'     : '',
        'visualization' : '',
        'seed'          : 0,
        'extra_args'    : [],
    }

    def __init__(self, is_single_command):
        self.clh = CommandLineHandler(sys.argv, vis_u.OPTIONS, True)
        self.clh.popFrontArgs()

        if is_single_command:
            pass
        else:
            if self.clh.getArgCount() < 2:
                self.clh.printUsageTable()
                sys.exit()
            else:
                algorithm = self.clh.getString()
                self.clh.validateOption('algorithms', algorithm)
                self.params['algorithm'] = algorithm

                visualization = self.clh.getString()
                self.clh.validateOption('visualizations', visualization)
                self.params['visualization'] = visualization

                if self.clh.validateArgsLength():
                    seed = self.clh.getInt()
                    self.clh.validateOption('seed', seed)
                    self.params['seed'] = seed


    def __getitem__(self, key):
        return self.params[key]
    
    def __setitem__(self, key, value):
        self.params[key] = value
