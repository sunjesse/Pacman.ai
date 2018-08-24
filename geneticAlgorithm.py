import numpy as np
import random
import pickle
from neuralnet import Neural

def populate(count, layerOneNeurons, layerTwoNeurons):
    population = []

    for i in range(0, count):
        net = Neural()
        for i in range(layerOneNeurons):
            net.weights_layer_1 = np.append(net.weights_layer_1, random.uniform(-1, 1))
        for i in range(layerTwoNeurons):
            net.weights_layer_2 = np.append(net.weights_layer_2, random.uniform(-1, 1))
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
