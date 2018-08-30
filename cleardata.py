import shelve

filename='shelve'
shelf = shelve.open(filename)
try:
    shelf["current_generation"] = 1
    shelf["1"] = []
finally:
    shelf.close()
