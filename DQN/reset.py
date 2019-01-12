import shelve
import csv

shelf = shelve.open("objects")

try:
    shelf["q_network"] = []
    shelf["target_network"] = []
    shelf["replay_buffer"] = []
    shelf["replay_buffer_two"] = []
    shelf["count"] = 0
    shelf["count_two"] = 0

finally:
    print("Erased all objects.")
    shelf.close()

f = open("training_data.csv", "w")
f.truncate()
f.close()
print("Erased all data.")
