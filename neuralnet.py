import random
import numpy as np

class Neural():

    def __init__(self):
        super(Neural, self).__init__()

        self.weights_layer_1 = np.array([]).T #Randomize
        self.weights_layer_2 = np.array([]).T #Randomize

        self.fitness = 0
