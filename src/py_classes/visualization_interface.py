from src.py_classes.accessor import Accessor
from abc import abstractmethod
from subprocess import run

class VisualizationInterface:
    accessor: Accessor = None
    params = {}

    def __init__(self, accessor, params):
        self.accessor = accessor
        self.params.update(params)
        self.params['seed_increment'] = accessor['optionInfo'].OPTIONS['default_seed_increment']

    @abstractmethod
    def getParamList(self):
        pass

    @abstractmethod
    def generate(self):
        pass

    @abstractmethod
    def open(self):
        pass

