# generate gif of random 3d points connected by lines to generate animated random 3d path
# 
# inputs:
#   max_step_size
#   max_step_angle
#   gif looping?
# 
# first frame will generate a random point
#   - each subsequent frame will advance point by some random length step 
#     at some random angle from the previous point

# TODO: 
#   have colors change for individual points / lines
#   implement color modes & color maps
#   ** might have to switch matplotlib -> plotly

from src.py_classes.vis_imports import *

class Vis_3d_walk(VisualizationInterface):
    def __init__(self, accessor, params):
        super().__init__(accessor, params)
    
        self.MAX_FRAMES = 500 # limit maximum number of .gif frames
        self.N = 100 # default scalar for random values
        self.debug = False

    def getParamList(self):
        return ['steps', 'stepSize', 'colorMap', 'useGif', 'loopGif', 'gifDuration', 'openPlotAfterGif']

    def getOptionInput(self, option):
        match option:
            case 'steps':
                return InputHandler.getIntFromInput("Maximum Number of Steps: ")
            case 'stepSize':
                return InputHandler.getIntFromInput("Maximum Step Size: ")
            case _:
                return ''

    def generate(self):
        # clear any warnings
        os.system('clear')

        steps = self['steps']
        N = self.N
        max_step_size = self['stepSize']
        self['heatmapPath'] = 'heatmaps/' + str(self['algorithm']) + '_' + str(steps) + 'x' + str(max_step_size) + '_3d_walk_frame.gif'

        # get random numbers
        scale = 6
        values = steps * scale
        randoms = self.accessor['cppHandler'].getNumbers(values)
        if (self.debug): 
            print("Randoms----------")
            print(randoms)
            print("-----------------")

        # unpack random data
        x = []
        y = []
        z = []
        s1 = []
        s2 = []
        s3 = []
        color = []
        for i in range(steps):
            if randoms[(i*scale)+3] >= 0.5: s1.append(1)
            else: s1.append(-1)
            if randoms[(i*scale)+4] >= 0.5: s2.append(1)
            else: s2.append(-1)
            if randoms[(i*scale)+5] >= 0.5: s3.append(1)
            else: s3.append(-1)
            if (i == 0):
                x.append(round(randoms[(i*scale)]*N))
                y.append(round(randoms[(i*scale)+1]*N))
                z.append(round(randoms[(i*scale)+2]*N))
            else:
                x.append(round(x[i-1] + randoms[(i*scale)] * max_step_size * s1[i], 2))
                y.append(round(y[i-1] + randoms[(i*scale)+1] * max_step_size * s2[i], 2))
                z.append(round(z[i-1] + randoms[(i*scale)+2] * max_step_size * s3[i], 2))

            color.append(i/steps) # gradient from start point -> end point

        if (self.debug):
            print("-------X--------")
            print(x)
            print("-------Y--------")
            print(y)
            print("-------Z--------")
            print(z)
            print("---------------")

        # generate .gif from .png frames of random walk steps
        if (self['useGif']):
            framePaths = []
            for step in range(0, steps):
                # step: (x, y, z) +- randomInt [0, max_step_size)

                # display progress
                if (not self.debug): print("Generating GIF... " + str(round(100 * (step / steps))) + "%")

                # generate plot frame
                ax = plt.axes(projection='3d')
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')
                ax.set_title('Random 3D Walk Step ' + str(step) + ' from ' + self['algorithm'].upper())
                if (step > 0): ax.plot3D(x[0:step], y[0:step], z[0:step], marker='o', c='0.5')
                ax.scatter3D(x[0:step], y[0:step], z[0:step], c=color[0:step], cmap=self['colorMap'], alpha=0.8)

                # save plot
                walkPath = 'heatmaps/3d_walk/' + str(self['algorithm']) + '_' + str(steps) + 'x' + str(max_step_size) + '_3d_walk_frame' + str(step) + '.png'
                framePaths.append(walkPath)
                plt.savefig(walkPath)
                if (step != steps-1): # dont clear last frame plot
                    plt.close()

                # clear progress for next update
                if (not self.debug): os.system('clear')

            # generate .gif from frames
            frames = []
            for png_path in framePaths:
                # convert to .png and open
                img = Image.open(png_path)
                frames.append(img)
            gifPath = 'heatmaps/' + str(self['algorithm']) + '_' + str(steps) + 'x' + str(max_step_size) + '_3d_walk_frame.gif'
            frames[0].save(gifPath, save_all=True, append_images=frames[1:], loop=(not self['loopGif']), duration=self['gifDuration']) # duration=gifDuration

            # clean up pngs
            for file in os.listdir('heatmaps/3d_walk'):
                if file.endswith('.png'):
                    os.remove('heatmaps/3d_walk/' + file)

            plt.close()

        # initialize plot
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

        # Horizontal slider to control number of points displayed
        axNumPoints = fig.add_axes([0.25, 0.1, 0.65, 0.03])
        self['numPoints_slider'] = Slider(
            ax=axNumPoints,
            label='Random Steps',
            valmin=0,
            valmax=steps,
            valinit=round(steps / 10),
        )
        # Vertical slider to control size of random points
        axPointSize = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
        self['pointSize_slider'] = Slider(
            ax=axPointSize,
            label='Point Size',
            valmin=0.1,
            valmax=100,
            valinit=25,
            orientation='vertical'
        )
        
        # register update function with NumPoints slider
        self['numPoints_slider'].on_changed(self.update)
        self['pointSize_slider'].on_changed(self.update)

        # initialize plot
        values = round(self['numPoints_slider'].val)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        if (values > 0): ax.plot3D(x[0:values], y[0:values], z[0:values], marker='o', c='0.5')
        ax.scatter3D(x[0:values], y[0:values], z[0:values], c=color[0:values], cmap=self['colorMap'], alpha=0.8)

        self['ax'] = ax
        self['x'] = x
        self['y'] = y
        self['z'] = z
        self['color'] = color

    # update plot when slider value changes
    def update(self, val):
        values = round(self['numPoints_slider'].val)
        self['ax'].cla()
        self['ax'].scatter3D(
            self['x'][0:values], 
            self['y'][0:values], 
            self['z'][0:values], 
            s=self['pointSize_slider'].val, 
            c=self['color'][0:values], 
            marker='o', 
            cmap=self['colorMap'], 
            alpha=0.8
        )
        if (values > 0): 
            self['ax'].plot3D(self['x'][0:values], self['y'][0:values], self['z'][0:values], marker=',', c='0.6')


    def open(self):
        super().open()
        if self['openPlotAfterGif']: 
            plt.show()