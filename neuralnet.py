import random
import numpy as np

class Neural():

    def __init__(self):
        super(Neural, self).__init__()

        self.weights_layer_1 = np.array([])#Randomize
        self.weights_layer_2 = np.array([])#Randomize

        self.fitness = 0

    def relu(self, x):
        return x * (x>0)

    def drelu(self, x):
        return 1 * (x>0)

    def process(self, input):
        a1 = self.relu(np.dot(self.weights_layer_1, input))
        output = np.dot(self.weights_layer_2, a1)
        return list(output).index(np.amax(output))

    def show(self, input):
        a1 = self.relu(np.dot(self.weights_layer_1, input))
        output = np.dot(self.weights_layer_2, a1)
        return output