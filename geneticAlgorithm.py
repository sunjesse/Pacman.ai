import numpy as np
import random
import pickle
from neuralnet import Neural

def populate(count, layerOneNeurons, layerTwoNeurons, layerThreeNeurons, outputNeurons):
    population = []

    for i in range(0, count): #dimension of weight matrix from layer i to layer j is neurons in i * neurons in j.
        net = Neural()
        net.weights_layer_1 = np.empty((0, layerOneNeurons), int)
        net.weights_layer_2 = np.empty((0, layerTwoNeurons), int)
        net.weights_layer_3 = np.empty((0, layerThreeNeurons), int)
        for j in range(layerTwoNeurons):
            row = []
            for i in range(layerOneNeurons):
                row.append(random.uniform(-1, 1))
            net.weights_layer_1 = np.vstack((net.weights_layer_1, row))

        for x in range(layerThreeNeurons):
            row2 = []
            for y in range(layerTwoNeurons):
                row2.append(random.uniform(-1, 1))
            net.weights_layer_2 = np.vstack((net.weights_layer_2, row2))

        for m in range(outputNeurons):
            row = []
            for n in range(layerThreeNeurons):
                row.append(random.uniform(-1, 1))
            net.weights_layer_3 = np.vstack((net.weights_layer_3, row))

        population.append(net)

    return population


def crossover(num_of_children, net_one, net_two):
    #Crossover the weights of two neural networks. Returns 2 child networksself.

    neuron_one = len(net_one.weights_layer_1[0]) #number of neurons in layer 1
    neuron_two = len(net_one.weights_layer_2[0]) #number of neurons in layer 2
    neuron_three = len(net_one.weights_layer_3[0])
    output_neurons = len(net_one.weights_layer_2)

    new_nets = []

    for i in range(num_of_children):
        child = Neural()
        child.weights_layer_1 = np.empty((0, neuron_one))
        child.weights_layer_2 = np.empty((0, neuron_two))
        child.weights_layer_3 = np.empty((0, neuron_three))

        for j in range(neuron_two): #layer 1 to 2 weights.
            row = []
            for i in range(neuron_one):
                if random.randint(0, 100) >= 50:
                    row.append(net_one.weights_layer_1[j][i]) #sample from net_one
                else:
                    row.append(net_two.weights_layer_1[j][i]) #sample from net_two
            child.weights_layer_1 = np.vstack((child.weights_layer_1, row))

        for j in range(neuron_three):
            row = []
            for i in range(neuron_two):
                if random.randint(0, 100) >= 50:
                    row.append(net_one.weights_layer_2[j][i])
                else:
                    row.append(net_two.weights_layer_2[j][i])
            child.weights_layer_2 = np.vstack((child.weights_layer_2, row))

        for j in range(output_neurons):
            row = []
            for i in range(neuron_three):
                if random.randint(0, 100) >= 50:
                    row.append(net_one.weights_layer_3[j][i])
                else:
                    row.append(net_two.weights_layer_3[j][i])
            child.weights_layer_3 = np.vstack((child.weights_layer_3, row))

        new_nets.append(child)

    return new_nets

def mutate(net): #Usage: replace old network with new mutated network when assigning to a list.
    #apply mutation algorithm
    neuron_one = len(net.weights_layer_1[0]) #number of neurons in layer 1
    neuron_two = len(net.weights_layer_2[0]) #number of neurons in layer 2
    neuron_three = len(net.weights_layer_3[0])
    output_neurons = len(net.weights_layer_2)

    mutated_network = net

    #layers = [net.weights_layer_1, net.weights_layer_2]

    for i in range(1, len(net.weights_layer_1)):
        x = random.randint(0, 100)
        if x <= 33: #mutate a weight in first layer
            mutated_network.weights_layer_1[random.randint(0, neuron_two-1)][random.randint(0, neuron_one-1)] = random.uniform(-1, 1)
        elif 33 < x <= 66: #mutate a weight in second layer
            mutated_network.weights_layer_2[random.randint(0, neuron_three-1)][random.randint(0, neuron_two-1)] = random.uniform(-1, 1)
        else:
            mutated_network.weights_layer_3[random.randint(0, output_neurons-1)][random.randint(0, neuron_three-1)] = random.uniform(-1, 1)

    return mutated_network

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
