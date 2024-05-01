import sys

class CommandLineHandler:
    
    OPTIONS = {}
    verbose = True
    args = []

    def __init__(self, args, OPTIONS, verbose):
        self.args = args
        self.OPTIONS = OPTIONS
        self.verbose = verbose

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
            "\n".join(self.OPTIONS['algorithms']),
            "",
            "Visualization Options: ",
            "-------------------------",
            "\n".join(self.OPTIONS['visualizations']),
            "",
        ]
        print("\n".join(message))

    def validateOption(self, option, value):
        result = True
        if (callable(self.OPTIONS[option])):
            if (not self.OPTIONS[option](value) and self.verbose):
                print("Invalid " + option)
                result = False
        else:
            if (not (value in self.OPTIONS[option]) and self.verbose):
                print("Invalid " + option + " -- Select From: ")
                print("----------------------------------")
                "\n".join(self.OPTIONS[option])
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

            



        

