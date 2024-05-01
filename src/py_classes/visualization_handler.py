from src.py_classes.imports import *
from src.py_classes.vis_imports import *

class VisualizationHandler:

    is_single_command = False
    visualization : VisualizationInterface = None
    optionInfo : OptionInfo = None

    def __init__(self, accessor: Accessor, is_single_command):
        self.accessor = accessor
        self.is_single_command = is_single_command
        self.verbose = not is_single_command
        self.optionInfo = self.accessor['optionInfo']

    def validateOption(self, option, value):
        result = True
        opt = self.optionInfo.OPTIONS[option]
        if (callable(opt)):
            if ((not opt(value)) and self.verbose):
                print("Invalid " + option)
                result = False
        else:
            if (not (value in self.optionInfo.OPTIONS[option]) and self.verbose):
                print("Invalid " + option + " -- Select From: ")
                print("----------------------------------")
                self.optionInfo.getOptionsString(option, "\n"),
                result = False
        return result
    
    def setup(self, params):
        vis = params['visualization']
        # create visualization object
        self.visualization = self.optionInfo.visualizations[vis](self.accessor, params)

        # get list of requirements
        req = self.visualization.getParamList()

        # get values for every requirement
        if self.is_single_command:
            pass
        else:
            for item in req:
                self.visualization.params[item] = self.getOptionInput(item)

    def run(self):
        self.visualization.generate()

    def open(self):
        self.visualization.open()

    def getOptionInput(self, option):
        match option:
            case 'rows':
                return InputHandler.getIntFromInput("Number of Rows: ")
            case 'columns':
                return InputHandler.getIntFromInput("Number of Columns: ")
            case 'colorMap':
                print("\nColor Map Options -- Select From:")
                print("\t" + self.optionInfo.getOptionsString('color_maps', "\n\t"))
                return InputHandler.getItemFromListFromInput("Color Map: ", self.optionInfo.OPTIONS['color_maps'])
            case 'points':
                return InputHandler.getIntFromInput("Number of Points: ")
            case 'interpolation':
                return InputHandler.getBoolFromInput("Interpolate? (Y/N): ")
            case 'interpolationPoints':
                if self.visualization.params['interpolation']:
                    return InputHandler.getIntFromInput("Number of Interpolation Points (Higher = Smoother): ")
                else:
                    return 0
            case 'maxPoints':
                return InputHandler.getIntFromInput("Maximum Number of Random Points: ")
            case 'colorMode':
                modified_color_modes = self.optionInfo.OPTIONS['color_mode_names'][:]
                for i in range(len(modified_color_modes)):
                    modified_color_modes[i] = str(i+1) + "= " + str(modified_color_modes[i])
                print("\nColor Mode Options -- Select From:")
                print("\t" + "\n\t".join(modified_color_modes))
                return InputHandler.getItemFromListFromInput("Color Mode: ", self.optionInfo.OPTIONS['color_modes'], modified_color_modes)
            case 'useGif':
                return InputHandler.getBoolFromInput("Would you like to generate a .gif? (Y/N): ")
            case 'loopGif':
                if self.visualization.params['useGif']:
                    return InputHandler.getBoolFromInput("GIF Looping? (Y/N): ")
                else:
                    return False
            case 'gifDuration':
                if self.visualization.params['useGif']:
                    return InputHandler.getFloatFromInput("GIF Duration: ")
                else:
                    return 0.0
            case '':
                pass
            case '':
                pass
            case '':
                pass
            case '':
                pass
            case _:
                pass
        return ''


