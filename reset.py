import shelve

filename='shelve'
shelf = shelve.open(filename)

for net in shelf["3"]:
    net.fitness = 0
shelf.close()
