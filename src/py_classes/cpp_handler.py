from subprocess import run
from src.py_classes.imports import *

class CppHandler:
    vebose = True

    def __init__(self, accessor, verbose = True):
        self.verbose = verbose
        self.accessor = accessor

    # rebuilds prng.cpp objects via makefile if necessary
    def makeIfNeeded(self):
        try:
            run('./prng -f data/output.txt', shell=True, check=True)
            return
        except:
            if self.vebose:
                print('Rebuilding ./prng ...')
            run('Make clean', shell=True)
            run('Make', shell=True)
            return
        
    
    def getNumbers(self, n):
        params = self.accessor.params
        OPTIONS = self.accessor['optionInfo'].OPTIONS
        try: #filter out bad inputs
            s = int(params['seed'])
            n = int(n)
            if (s < 0) or (n <= 0): 
                return -1
        except ValueError: 
            return -1
        algo = params['algorithm']
        if (algo not in OPTIONS['algorithms']): return -1

        # get random scalars from ./prng
        filePath = "data/output.txt"

        # IMPORTANT: add case for each algorithm that requires extra arguments
        if algo not in OPTIONS['has_extra_args']:
            cmd = './prng -f ' + filePath + ' -a ' + str(algo.lower()) + ' -s ' + str(s) + ' -n ' + str(n)
        else:
            cmd = './prng -f ' + filePath + ' -a lfg -s ' + str(s) + ' -n ' + str(n) + ' -O \"' + ",".join(params['extra_args']) + '\"'
        run(cmd, shell=True)
        nums = np.genfromtxt(filePath)
        if (nums.size == 1): randoms = [nums.item()]
        else: randoms = list(nums)
        return randoms

