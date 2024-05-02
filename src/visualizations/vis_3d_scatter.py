# Interactive 3D scatter plot of randomly generated 3D points
#
# Visuals are called from main.py with initial parameters algorithm and seed:
#   python3 3d_scatter.py (algorithm) (seed)
#
# additional parameters (from standard input):
#   maximum number of points
#   color map
#   color mode
#
# sliders (for interactive 3D plot):
#    number of points shown
#    size of points
# 
# can use native matplotlib zoom to explore distribution of random points

from pylab import *

from src.py_classes.vis_imports import *

class Vis_3d_scatter(VisualizationInterface):
    def __init__(self, accessor, params):
        super().__init__(accessor, params)
    
        self.MAX_FRAMES = 500 # limit maximum number of .gif frames
        self.N = 100 # default scalar for random values
        self.debug = False

    def getParamList(self):
        return ['maxPoints', 'colorMap', 'colorMode', 'useGif', 'loopGif', 'gifDuration']

    def generate(self):
        colorMode = self['colorMode']
        colorMap = self['colorMap']
        MAX_VALUES = self['maxPoints']
        MAX_FRAMES = self.MAX_FRAMES
        N = self.N

        self['heatmapPath'] = 'heatmaps/' + str(self['algorithm']) + '3d_scatter_' + str(MAX_VALUES) + '.gif'

        # STEP 2: Generate data for visualization via prng.cpp calls
        data = []
        if (colorMode == 1): 
            numAxis = 4 
        else: 
            numAxis = 3
        
        all_data = self.accessor['cppHandler'].getNumbers(MAX_VALUES*numAxis)

        for i in range(numAxis):
            axis = all_data[(i*MAX_VALUES):((i+1)*MAX_VALUES)]
            for i in range(MAX_VALUES): axis[i] = axis[i] * N # scale values
            data.append(axis) # append axis of numVals values scaled to [0, N)

        # STEP 3: Generate visualization
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

        # Horizontal slider to control number of points displayed
        axNumPoints = fig.add_axes([0.25, 0.1, 0.65, 0.03])
        self['numPoints_slider'] = Slider(
            ax=axNumPoints,
            label='Random Points',
            valmin=0,
            valmax=MAX_VALUES,
            valinit=round(MAX_VALUES / 10),
        )
        # Vertical slider to control size of random points
        axPointSize = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
        self['pointSize_slider'] = Slider(
            ax=axPointSize,
            label='Point Size',
            valmin=0.1,
            valmax=50,
            valinit=1,
            orientation='vertical'
        )
        
        # register update function with NumPoints slider
        self['numPoints_slider'].on_changed(self.update)
        self['pointSize_slider'].on_changed(self.update)

        # unpack data / colors
        x = data[0]
        y = data[1]
        z = data[2]
        if (colorMode == 1): # random
            color = data[3] 
        elif (colorMode == 2): # diagonal gradient
            color = [0] * MAX_VALUES
            for i in range(MAX_VALUES):
                color[i] = (x[i] + y[i] + z[i])
        elif (colorMode == 3):  # x gradient
            color = x.copy()
        elif (colorMode == 4): # y gradient
            color = y.copy()
        elif (colorMode == 5): # z gradient
            color = z.copy()
        else :
            print('Fatal Error: missing color mode')
            sys.exit()
        
        if (self['useGif']):
            # display progress

            # generate .gif frames
            plt.close()
            framePaths = []
            frames = []
            numFrames = min(MAX_VALUES, MAX_FRAMES)
            if (numFrames == MAX_VALUES): 
                valuesPerFrame = 1
            else: 
                valuesPerFrame = MAX_VALUES // MAX_FRAMES
            for n in range(numFrames):
                if (not self.debug): 
                    print("Generating GIF... " + str(round(100 * (n / numFrames))) + "%")
                i = n*valuesPerFrame
                fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
                ax.scatter(
                    x[0:i], 
                    y[0:i], 
                    z[0:i], 
                    c=color[0:i], 
                    marker='o', 
                    cmap=colorMap, 
                    alpha=1
                )
                self['heatmap_temp'] = 'heatmaps/3d_scatter/' + str(self['algorithm']) + '_3d_scatter_frame_' + str(i) + '.png'
                framePaths.append(self['heatmap_temp'])
                plt.savefig(self['heatmap_temp'])
                plt.close()

                # clear progress for next update
                if (not self.debug): 
                    os.system('clear')

            # STEP 5: Open .png frames to generate .gif from numIterations 
            for png_path in framePaths:
                # convert to .png and open
                img = Image.open(png_path)
                frames.append(img)

            # generate .gif
            self['heatmapPath'] = 'heatmaps/' + str(self['algorithm']) + '3d_scatter_' + str(MAX_VALUES) + '.gif'
            frames[0].save(self['heatmapPath'], save_all=True, append_images=frames[1:], loop=(not self['loopGif']), duration=self['gifDuration']) # duration=gifDuration

        # set params so we can open later
        self['ax'] = ax
        self['x'] = x
        self['y'] = y
        self['z'] = z
        self['color'] = color

    # update plot when slider value changes
    def update(self, val):
        values = round(self['numPoints_slider'].val)
        self['ax'].cla()
        self['ax'].scatter(
            self['x'][0:values], 
            self['y'][0:values], 
            self['z'][0:values], 
            s=self['pointSize_slider'].val, 
            c=self['color'][0:values], 
            marker='o', 
            cmap=self['colorMap'], 
            alpha=1
        )

    def open(self):
        # clean up pngs
        for file in os.listdir('heatmaps/3d_scatter'):
            if file.endswith('.png'):
                os.remove('heatmaps/3d_scatter/' + file)

        # open .gif
        cmd = 'open ' + self['heatmapPath']
        run(cmd, shell=True)

        # initialize plot
        values = round(self['numPoints_slider'].val)
        self['ax'].scatter(
            self['x'][0:values], 
            self['y'][0:values], 
            self['z'][0:values], 
            c=self['color'][0:values], 
            marker='o', 
            cmap=self['colorMap'], 
            alpha=1
        )
        plt.show()


