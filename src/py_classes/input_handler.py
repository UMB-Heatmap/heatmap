import sys

class InputHandler:
    params = {
        'algorithm'     : '',
        'visualization' : '',
        'seed'          : 12345,
    }
    extra_args = []

    OPTIONS = {}
    option_order = []

    verbose = True

    def __init__(self, options, args, option_order = []):
        self.OPTIONS = options

        # check for args
        if (len(args) < 2):
            self.printUsageTable()
            sys.exit()

        # used for running the script in a single line and returning errors in json format
        if (args[1] == "-all"):
            if (len(args < 3)):
                # TODO throw error
                sys.exit()
            self.verbose = False
            self.option_order = option_order
            # pass rest of args
            self.extra_args = self.handleAll(args[2:])

        # default mode
        else:
            self.verbose = True
            # pass rest of args
            self.handleSimple(args[1:])
    
    def __getitem__(self, key):
        return self.params[key]
    
    def __setitem__(self, key, value):
        self.params[key] = value
        
    def handleAll(self, args):
        # check args length
        num = len(self.option_order)
        if (len(args) < num):
            # TODO throw json error
            pass

        # validate every option
        i = 0
        while (i < num):
            opt = self.option_order[i]
            val = args[i]
            if (not self.validateOption(opt, val)):
                # TODO throw json error
                pass
            self[opt] = val
            i += 1
        
        # return extra args
        if (len(args) > num):
            return args[i:]
        else:
            return []


    def handleSimple(self, args):
        # check for args
        if(len(args) < 2):
            self.printUsageTable()
            sys.exit()

        self['algorithm'] = args[0]
        if (not self.validateOption('algorithm', self['algorithm'])):
            exit()

        self['visualization'] = args[1]
        if (not self.validateOption('visualization', self['visualization'])):
            exit()

        if (len(args) == 3):
            if (not self.validateSeed(args[2])):
                exit()
            self['seed'] = int(args[2])
        
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
            "\n".join(self.OPTIONS['algorithms']),
            "",
            "Visualization Options: ",
            "-------------------------",
            "\n".join(self.OPTIONS['visualizations']),
            "",
        ]
        print("\n".join(message))

    def validateOption(self, option, value):
        result = (value not in self.OPTIONS[option])
        if (result and self.verbose):
            print("Invalid " + option + " -- Select From: ")
            print("----------------------------------")
            "\n".join(self.OPTIONS[option])
        return result

    def validateSeed(self, seed):
        result = True
        try:
            seed = int(seed)
        except ValueError:
            result = False
            if (self.verbose):
                print("Invalid Seed -- Must be Integer")
        return result

    

        

