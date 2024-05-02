# seed_eval HEATMAP VISUALIZATION:
#   generates N x M heatmap of random numbers with N random seeds

# Visuals are called from main.py with initial parameters algorithm and seed:
#   python3 2d.py (algorithm) (seed)

# Any additional visualization-specific parameters should be acquired 
# within said visualization script by prompting the user via standard input

# 2D Visualization requires 5 additional inputs:
#   number_of_rows, number_of_columns, color_map, minSeed, maxSeed

from src.py_classes.vis_imports import *

class Vis_SeedEval(VisualizationInterface):
    def __init__(self, accessor, params):
        super().__init__(accessor, params)
    
        self['initalSeed'] = params['seed']

    def getParamList(self):
        return ['minSeed', 'maxSeed', 'rows_', 'columns', 'colorMap']
    
    def getOptionInput(self, option):
        match option:
            case 'minSeed':
                return InputHandler.getIntFromInput("Minimum seed value: ")
            case 'maxSeed':
                return InputHandler.getIntFromInput("Minimum seed value: ")
            case 'rows_':
                val = InputHandler.getIntFromInput("Number of rows: ")
                while int(abs(self['maxSeed'] - self['minSeed']) / val) == 0:
                    val = InputHandler.getIntFromInput("Number of rows cannot be greater than the difference of min and max seed values: ")
                return val
            case _:
                return ''

    def generate(self):
        minSeed = self['minSeed']
        maxSeed = self['maxSeed']
        numRows = self['rows_']
        numCols = self['columns']

        # STEP 2: Generate data for visualization via ./prng calls (abstracted to vis.nRandomScalars)
        seeds = [*range(minSeed, maxSeed+1, int(abs(maxSeed - minSeed) / numRows))]
        seeds = seeds[:numRows]
        seeds.sort(reverse=True)
        data = []
        for n in range(numRows):
            self.accessor.params['seed'] = seeds[n]
            row = self.accessor['cppHandler'].getNumbers(numCols)
            data.append(row)

        # STEP 3: Generate visualization
        ticks = []
        tick_labels = []
        plt.ylabel("Seed")
        if (numRows > 25): # maximum 25 seed row labels (more than that looks cluttered)
            spacing =  numRows // (25 - 1)
            for x in range(25):
                ticks.append(int(x*spacing))
                tick_labels.append(seeds[int(x*spacing)])
        else:
            ticks = [*range(0, numRows)]
            tick_labels = seeds
        plt.yticks(ticks, tick_labels)
        plt.imshow(data, cmap=self['colorMap'])
        plt.title(str(numRows) + "x" + str(numCols) + " Heat Map from " + self['algorithm'].upper())
        plt.colorbar()

        # STEP 4: Save visualization in heatmaps folder with appropriate name
        self['heatmapPath'] = 'heatmaps/' + str(self['algorithm']) + '_' + str(numRows) + 'x' + str(numCols) + '_2d_heatmap.svg'
        plt.savefig(self['heatmapPath'])

