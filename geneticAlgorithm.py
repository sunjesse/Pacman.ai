import numpy as np
import random
import pickle
from neuralnet import Neural

def populate(count, layerOneNeurons, layerTwoNeurons, outputNeurons):
    population = []

    for i in range(0, count): #dimension of weight matrix from layer i to layer j is neurons in i * neurons in j.
        net = Neural()
        net.weights_layer_1 = np.empty((0, layerOneNeurons), int)
        net.weights_layer_2 = np.empty((0, layerTwoNeurons), int)
        for j in range(4):
            row = []
            for i in range(5):
                row.append(random.uniform(-1, 1))
            net.weights_layer_1 = np.vstack((net.weights_layer_1, row))

        for x in range(4):
            row2 = []
            for y in range(4):
                row2.append(random.uniform(-1, 1))
            net.weights_layer_2 = np.vstack((net.weights_layer_2, row2))
        population.append(net)

    return population

def calculateFitness():
    return

def crossover(net_one, net_two):
    #Crossover the weights of two neural networks. Returns 2 child networksself.
    return

def mutate(net):
    #apply mutation algorithm
    return

def selection(population):
    #return network(s) with highest fitness
    return

def evolve(population):
    return

def save_data(dataset):
    data = dataset
    output_file = "training.data"
    fw = open(output_file, 'wb')
    pickle.dump(data, fw)
    fw.close()

def load_data():
    input_file = 'training.data'
    fd = open(input_file, 'rb')
    data = pickle.load(fd)
    return data
