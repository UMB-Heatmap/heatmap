# 3D HEATMAP VISUALIZATION WITH INTERPOLATION:
#   generates N number of heatmap of random numbers

# Visuals are called from main.py with initial parameters algorithm and seed:
#   python3 3d.py (algorithm) (seed)

# Any additional visualization-specific parameters should be acquired 
# within said visualization script by prompting the user via standard input

# 3D Visualization requires 3 additional inputs:
#   number_of_points, number_of_interpolation_points, color_map



from src.py_classes.vis_imports import *

class Vis_3d(VisualizationInterface):
    def getParamList(self):
        return ['points', 'interpolation', 'interpolationPoints', 'colorMap']

    def generate(self):
        # This only serves to fix an error down the line
        colorMap1 = plt.colormaps.get_cmap(self.params['colorMap'])

        numP = self.params['points']

        # STEP 1: Generate data for visualization via prng.cpp calls
        #   to get NUM_VALUES random doubles in range [0, 1) using ALGORITHM and SEED:
        #       ./prng -f data/OUTPUT_FILENAME.txt -a ALGORITHM -s SEED -n NUM_VALUES
        #   then read random numbers from txt file data/OUTPUT_FILENAME.txt 
        #   NOTE: output txt files are meant as intermediate data storage so naming is arbitrary
        data = []
        all_data = self.accessor['cppHandler'].getNumbers(numP * numP)
        for x in range(numP):
            row = all_data[(x*numP):((x+1)*numP)]
            data.append(row)

        # STEP 2: Generate visualization

        # Set up plot
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

        ax.set(
            xlabel='X',
            ylabel='Y',
            zlabel='Z',
        )

        # Original Heatmap without interpolation
        X = np.linspace(0, 1, numP)
        Y = np.linspace(0, 1, numP)
        X, Y = np.meshgrid(X, Y)
        Z = np.asarray(data)

        if (self.params['interpolation']):
            interP = self.params['interpolationPoints']
            # Define new grid for interpolation
            newX, newY = np.mgrid[0:1:1j * interP, 0:1:1j * interP]

            # Perform interpolation
            tck = interpolate.bisplrep(X, Y, Z, s=0)  # Adjust 's' for smoothing level
            newZ = interpolate.bisplev(newX[:, 0], newY[0, :], tck)

            # Plot interpolated surface
            surf = ax.plot_surface(newX, newY, newZ, cmap=colorMap1, antialiased=True)

        else:
            # Plot surface
            surf = ax.plot_surface(X, Y, Z, cmap=colorMap1, antialiased=True)

        fig.colorbar(surf, ax=ax, fraction=0.02, pad=0.1, label=str(self.params['colorMap']))

        # STEP 3: Save visualization in heatmaps folder with appropriate name
        self.params['heatmapPath'] = 'heatmaps/' + str(self.params['algorithm']) + '_' + str(self.params['seed']) + '_3d_heatmap.svg'
        plt.title("3D Heat Map from " + self.params['algorithm'].upper())
        plt.savefig(self.params['heatmapPath'])

