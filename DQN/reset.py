import shelve
import csv

filename='object'
shelf = shelve.open(filename)

try:
    shelf["q_network"] = []
    shelf["target_network"] = []
    shelf["replay_buffer"] = []
    shelf["replay_buffer_two"] = []
    shelf["P"] = []
    shelf["P_two"] = []

finally:
    print("Erased all objects.")
    shelf.close()

f = open("training_data.csv", "w")
f.truncate()
f.close()
print("Erased all data.")
