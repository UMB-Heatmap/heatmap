from src.py_classes.imports import *

class CommandLineHandler:
    
    accessor: Accessor = None
    optionInfo = None

    OPTIONS = {}
    verbose = True
    args = []

    def __init__(self, accessor: Accessor, args, verbose):
        self.args = args
        # pop first item always
        self.popFrontArgs()

        self.accessor = accessor
        self.optionInfo = accessor['optionInfo']
        self.verbose = verbose

        self.OPTIONS = self.optionInfo.OPTIONS

    def getString(self):
        if not self.validateArgsLength():
            if self.verbose:
                self.printUsageTable()
            else:
                # TODO throw json error
                pass
            sys.exit()
        result = self.args[0]
        self.popFrontArgs()
        return result
    
    def getInt(self):
        if ((not self.validateArgsLength()) or (not self.validateInt(self.args[0]))):
            if self.verbose:
                self.printUsageTable()
            else:
                # TODO throw json error
                pass
            sys.exit()
        else:
            result = int(self.args[0])
            self.popFrontArgs()
            return result
        
    def popFrontArgs(self):
        if (len(self.args) > 1):
            self.args = self.args[1:]
        else:
            self.args = []

    # returns true if there are more items
    def validateArgsLength(self):
        return (len(self.args) > 0)
            
    def printUsageTable(self):
        message = [
            "",
            "Invalid Arguments -- Usage:",
            "-------------------------",
            "",
            "python3 main.py (algorithm) (visual) [seed : Int]",
            "",
            "PRNG Algorithm Options:  ",
            "-------------------------",
            self.optionInfo.getOptionsString('algorithms', "\n"),
            "",
            "Visualization Options: ",
            "-------------------------",
            self.optionInfo.getOptionsString('visualizations', "\n"),
            "",
        ]
        print("\n".join(message))

    def validateOption(self, option, value):
        result = True
        opt = self.OPTIONS[option]
        if (callable(opt)):
            if ((not opt(value)) and self.verbose):
                print("Invalid " + option)
                result = False
        else:
            if (not (value in self.OPTIONS[option]) and self.verbose):
                print("Invalid " + option + " -- Select From: ")
                print("----------------------------------")
                self.optionInfo.getOptionsString(option, "\n"),
                result = False
        return result

    def validateInt(self, value):
        result = True
        try:
            value = int(value)
        except ValueError:
            result = False
        return result
    
    def getArgCount(self):
        return len(self.args)

    def getCoreArgs(self, force_seed = False):
        print('Getting Core Args')
        print(self.args)
        if self.getArgCount() < 2:
            if self.verbose:
                self.printUsageTable()
            sys.exit()

        # set default values
        algorithm = ''
        visualization = ''
        seed = self.accessor['optionInfo'].OPTIONS['default_seed']

        # get algorithm
        algorithm = self.getString()
        self.validateOption('algorithms', algorithm)

        # get visualization
        visualization = self.getString()
        self.validateOption('visualizations', visualization)

        # get seed
        if (self.validateArgsLength() or force_seed):
            seed = self.getInt()
            self.validateOption('seed', seed)
        
        return [algorithm, visualization, seed]

    

        

