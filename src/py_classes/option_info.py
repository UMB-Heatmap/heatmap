import src.py_classes.extra_args_callbacks as eac
from src.py_classes.vis_exports import *

class OptionInfo:
    OPTIONS = {
        'algorithms'            : ['lehmer', 'splitmix', 'xorshift', 'lcg', 'middle_square', 'rule30', 'lfg', 'bbs', 'four'],
        'visualizations'        : ['2d', 'distribution', 'frequency', '3d_scatter', '3d_walk', '3d', 'shadedrelief', 'seed_eval'],
        'has_extra_args'        : ['lfg', 'bbs'],
        # Color Map Options (directly from MatPlotLib)
        # https://matplotlib.org/stable/gallery/color/colormap_reference.html
        'color_maps'            : ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink', 'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper'],
        'color_mode_names'      : ['random', 'diagonal gradient', 'x gradient', 'y gradient', 'z gradient'],
        'default_seed'          : 12345,
        'default_seed_increment': 12345,
    }

    callbacks = {
        'lfg' : eac.lfg_params,
        'bbs' : eac.bbs_params,
    }

    visualizations = {
        '2d'            : Vis_2d, 
        'distribution'  : None, 
        'frequency'     : None, 
        '3d_scatter'    : None, 
        '3d_walk'       : None, 
        '3d'            : None, 
        'shadedrelief'  : None, 
        'seed_eval'     : None,
    }

    def __init__(self):
        self.OPTIONS.update({
            # range(1, LENGTH_OF_color_mode_names + 1)
            'color_modes'       : range(1, len(self.OPTIONS['color_mode_names']) + 1),
            'seed'              : self.validateInt,
        })


    def validateInt(self, value):
        result = True
        try:
            value = int(value)
        except ValueError:
            result = False
        return result
    
    def getOptionsString(self, option, delimiter):
        return str(delimiter).join(self.OPTIONS[option])
