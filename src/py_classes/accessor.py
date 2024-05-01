from src.py_classes.imports import *

class Accessor:
    objects = {
        'commandLineHandler' : None,
        'optionInfo' : None,
        'visualizationRunner' : None,
        'inputHandler' : InputHandler
    }

    def __init__(self):
        pass

    def __setitem__(self, key, value):
        self.objects[key] = value

    def __getitem__(self, key):
        return self.objects[key]
