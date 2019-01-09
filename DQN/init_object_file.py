import shelve

shelf = shelve.open("objects")

try:
    shelf["first_time"] = True
finally:
    print("Initialized with value " + str(shelf["first_time"]) +  ".")
    shelf.close()
