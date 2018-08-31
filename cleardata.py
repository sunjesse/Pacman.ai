import shelve

filename='shelve'
shelf = shelve.open(filename)
try:
    shelf["current_generation"] = 1

    for i in range(1, shelf["current_generation"]): #clears all the best nets lists of each generation
        shelf[str(i)] = []
finally:
    shelf.close()
