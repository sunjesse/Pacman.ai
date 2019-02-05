import random
import numpy as np
import math

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

        self.alpha = 1
        self.temp = 1.0

        self.apply_softmax = True

    def sigmoid(self, x):
        return 1/(1+np.exp(-x))

    def d_sigmoid(self, x):
        sig_x = self.sigmoid(x)
        return sig_x*(1-sig_x)

    def relu(self, x):
        return x * (x>0)

    def d_relu(self, x):
        return 1 * (x>0)

    def softmax(self, array):
        sum = 0
        for i in array[0]:
            sum += math.exp(i/self.temp)
        soft = [math.exp(i/self.temp)/sum for i in array[0]]
        return soft

    def process(self, input):
        self.input_layer = np.array(input).reshape([self.layerOne, 1])
        self.activationTwo = self.sigmoid(np.dot(self.weights_layer_1, self.input_layer)).reshape([self.layerTwo, 1])
        self.activationThree = self.sigmoid(np.dot(self.weights_layer_2, self.activationTwo)).reshape([self.layerThree, 1])
        self.stateLayerFour = np.dot(self.weights_layer_3, self.activationThree).reshape([self.output, 1])
        #print(self.softmax(self.stateLayerFour.T))
        if self.apply_softmax:
            return self.softmax(self.stateLayerFour.T)
        return list(self.stateLayerFour).index(np.amax(self.stateLayerFour))

    def forward(self, input):
        self.input_layer = np.array(input).reshape([self.layerOne, 1])
        self.activationTwo = self.sigmoid(np.dot(self.weights_layer_1, self.input_layer)).reshape([self.layerTwo, 1])
        self.activationThree = self.sigmoid(np.dot(self.weights_layer_2, self.activationTwo)).reshape([self.layerThree, 1])
        self.stateLayerFour = np.dot(self.weights_layer_3, self.activationThree).reshape([self.output, 1])
        return list(self.stateLayerFour)

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
        return (1/self.output)*np.dot((np.array(y)-np.array(target_out)).T, (np.array(y)-np.array(target_out)))
        #return (1/self.output)*np.sum(np.multiply(y-target_out, y-target_out))

    def backpropagate(self, target_out, y):
        '''Apply softmax here??'''
        delta_four = (np.array(y)-np.array(target_out)) * self.d_sigmoid(self.stateLayerFour).reshape([self.output, 1]) #self.stateLayerFour == np.dot(self.weights_layer_3, self.activationThree)
        delta_three = np.multiply(np.dot(self.weights_layer_3.T, delta_four), self.d_sigmoid(self.activationThree)).reshape([self.layerThree, 1])
        delta_two = np.multiply(np.dot(self.weights_layer_2.T, delta_three), self.d_sigmoid(self.activationTwo)).reshape([self.layerTwo, 1])

        self.weights_layer_1 -= self.alpha*np.dot(np.array(self.input_layer), delta_two.T).T
        self.weights_layer_2 -= self.alpha*np.dot(self.activationTwo, delta_three.T).T
        self.weights_layer_3 -= self.alpha*np.dot(self.activationThree, delta_four.T).T
        print("Updated weights.")
        #delta_four = (np.array(y) - np.array(target_out)) * self.d_relu(self.target_out)
        #delta_three = np.dot(self.a)
