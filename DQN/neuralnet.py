import random
import numpy as np

class Neural():

    def __init__(self):
        super(Neural, self).__init__()

        self.weights_layer_1 = np.array([])#Randomize
        self.weights_layer_2 = np.array([])#Randomize
        self.weights_layer_3 = np.array([])#Randomize

        self.fitness = 0
        self.peak_fitness = 0

    def relu(self, x):
        return x * (x>0)

    def drelu(self, x):
        return 1 * (x>0)

    def process(self, input):
        a1 = self.relu(np.dot(self.weights_layer_1, input))
        a2 = self.relu(np.dot(self.weights_layer_2, a1))
        output = np.dot(self.weights_layer_3, a2)
        return list(output).index(np.amax(output))

    def show(self, input):
        a1 = self.relu(np.dot(self.weights_layer_1, input))
        a2 = self.relu(np.dot(self.weights_layer_2, a1))
        output = np.dot(self.weights_layer_3, a2)
        return output

    def init_weights(self, layerOneNeurons, layerTwoNeurons, layerThreeNeurons, outputNeurons): #randomly initialize the weights of the neural network.
        self.weights_layer_1 = np.empty((0, layerOneNeurons), int)
        self.weights_layer_2 = np.empty((0, layerTwoNeurons), int)
        self.weights_layer_3 = np.empty((0, layerThreeNeurons), int)
        for j in range(layerTwoNeurons):
            row = []
            for i in range(layerOneNeurons):
                row.append(random.uniform(-1, 1))
            self.weights_layer_1 = np.vstack((self.weights_layer_1, row))

        for x in range(layerThreeNeurons):
            row2 = []
            for y in range(layerTwoNeurons):
                row2.append(random.uniform(-1, 1))
            self.weights_layer_2 = np.vstack((self.weights_layer_2, row2))

        for m in range(outputNeurons):
            row = []
            for n in range(layerThreeNeurons):
                row.append(random.uniform(-1, 1))
            self.weights_layer_3 = np.vstack((self.weights_layer_3, row))
