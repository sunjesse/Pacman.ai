import shelve

shelf = shelve.open("objects")


shelf["first_time"] = True
print("Initialized with value " + str(shelf["first_time"]) +  ".")
shelf.close()
