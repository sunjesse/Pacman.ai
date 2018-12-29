import random
import numpy as np

class Neural():

    def __init__(self):
        super(Neural, self).__init__()

        self.weights_layer_1 = np.array([])#Randomize
        self.weights_layer_2 = np.array([])#Randomize
        self.weights_layer_3 = np.array([])#Randomize
        self.input_layer = np.array([]) #equal to input state vector
        self.activationTwo = np.array([])
        self.activationThree = np.array([])
        self.stateLayerFour = np.array([])

        self.layerOne = 0
        self.layerTwo = 0
        self.layerThree = 0
        self.output = 0

        self.fitness = 0
        self.peak_fitness = 0

        self.alpha = 1

    def relu(self, x):
        return x * (x>0)

    def drelu(self, x):
        return 1 * (x>0)

    def process(self, input):
        self.input_layer = input
        self.activationTwo = self.relu(np.dot(self.weights_layer_1, self.input_layer))
        self.activationThree = self.relu(np.dot(self.weights_layer_2, self.activationTwo))
        self.stateLayerFour = np.dot(self.weights_layer_3, self.activationThree)
        return list(output).index(np.amax(self.stateLayerFour))

    def show(self, input):
        self.input_layer = input
        self.activationTwo = self.relu(np.dot(self.weights_layer_1, self.input_layer))
        self.activationThree = self.relu(np.dot(self.weights_layer_2, self.activationTwo))
        self.stateLayerFour = np.dot(self.weights_layer_3, self.activationThree)
        return self.stateLayerFour

    def init_weights(self, layerOneNeurons, layerTwoNeurons, layerThreeNeurons, outputNeurons): #randomly initialize the weights of the neural network.
        self.layerOne = layerOneNeurons
        self.layerTwo = layerTwoNeurons
        self.layerThree = layerThreeNeurons
        self.output = outputNeurons

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

    def calculate_mse(self, target_out, y):
        return (1/self.output)*np.sum(np.multiply(y-target_out, y-target_out))

    def backpropagate(self, target_out, y):
        delta_four = np.dot(y-target_out, self.drelu(self.stateLayerFour)) #self.stateLayerFour == np.dot(self.weights_layer_3, self.activationThree)
        delta_three = np.multiply(np.dot(self.weights_layer_3, delta_four), self.drelu(np.dot(self.weights_layer_2, self.activationTwo)))
        delta_two = np.multiply(np.dot(self.weights_layer_2, delta_three), self.drelu(np.dot(self.weights_layer_1, self.input_layer)))

        self.weights_layer_1 += self.alpha*np.dot(self.input_layer, delta_two)
        self.weights_layer_2 += self.alpha*np.dot(self.activationTwo, delta_three)
        self.weights_layer_3 += self.alpha*np.dot(self.activationThree, delta_four)
