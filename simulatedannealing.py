'''
To Do:
1. Implement pseudorandom selection of networks in population and add it to list in the compute() function.
'''
import math
import random

class SimulatedAnnealing():

    def __init__(self):
        super(SimulatedAnnealing, self).__init__()
        self.temp = 0 #temp should be very low, like < 1

    def compute(list, best_networks, temperature): #list is a subset of networks in the population that pseudorandomly have been selected.
        self.temp = temperature
        returnList = best_networks
        for net in list:
            for best_nets in best_networks:
                if net.fitness < best_nets.fitness:
                    if random.uniform(0, 1) <= calculate_probability(best_nets.fitness, net.fitness):
                        returnList.append(net)
        return returnList


    def calculate_probability(fit1, fit2):
        return math.exp(-((fit2 - fit1)/self.temp))
