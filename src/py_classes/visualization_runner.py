from src.py_classes.imports import *

import sys

class VisualizationRunner:

    is_single_command = False

    params = {
        'algorithm'     : '',
        'visualization' : '',
        'seed'          : 0,
        'extra_args'    : [],
    }

    def __init__(self, accessor: Accessor, is_single_command):
        self.clh = accessor['commandLineHandler']
        accessor['commandLineHandler'].verbose = True
        self.clh.popFrontArgs()

        # single command only
        if is_single_command:
            pass

        # basic/normal usage
        else:
            if self.clh.getArgCount() < 2:
                self.clh.printUsageTable()
                sys.exit()
            else:
                self._getCoreArgs()

            if self['algorithm'] in accessor['optionInfo'].OPTIONS['has_extra_args']:
                accessor['optionInfo'].callbacks[self['algorithm']]()

    def __getitem__(self, key):
        return self.params[key]
    
    def __setitem__(self, key, value):
        self.params[key] = value

    def _getCoreArgs(self, force_seed = False):
        # get algorithm
        algorithm = self.clh.getString()
        self.clh.validateOption('algorithms', algorithm)
        self.params['algorithm'] = algorithm
        # get visualization
        visualization = self.clh.getString()
        self.clh.validateOption('visualizations', visualization)
        self.params['visualization'] = visualization
        # get seed
        if (self.clh.validateArgsLength() or force_seed):
            seed = self.clh.getInt()
            self.clh.validateOption('seed', seed)
            self.params['seed'] = seed
