# 2D HEATMAP VISUALIZATION:
#   generates N x M heatmap of random numbers

# Visuals are called from main.py with initial parameters algorithm and seed:
#   python3 2d.py (algorithm) (seed)

# Any additional visualization-specific parameters should be acquired 
# within said visualization script by prompting the user via standard input

# 2D Visualization requires 3 additional inputs:
#   number_of_rows, number_of_columns, color_map


from src.py_classes.vis_imports import *

class Vis_2d(VisualizationInterface):
    def __init__(self, accessor, params):
        super().__init__(accessor, params)

    def getParamList(self):
        return ['rows', 'columns', 'colorMap']
    
    def generate(self):
        numRows = self.params['rows']
        numCols = self.params['columns']
        colorMap = self.params['colorMap']

        # STEP 1: Generate data for visualization via ./prng calls (abstracted to vis.nRandomScalars)
        data = []
        all_data = self.accessor['cppHandler'].getNumbers(numRows * numCols)
        for n in range(numRows):
            row = all_data[(n*numCols):((n+1)*numCols)]
            data.append(row)

        # STEP 2: Generate visualization
        plt.imshow(data, cmap=colorMap)
        plt.title(str(numRows) + "x" + str(numCols) + " Heat Map from " + self.params['algorithm'].upper())
        plt.colorbar()

        # STEP 3: Save visualization in heatmaps folder with appropriate name
        self.params['heatmapPath'] = 'heatmaps/' + str(self.params['algorithm']) + '_' + str(numRows) + 'x' + str(numCols) + '_2d_heatmap.svg'
        plt.savefig(self.params['heatmapPath'])

    def open(self):
        cmd = 'open ' + self.params['heatmapPath']
        run(cmd, shell=True)

