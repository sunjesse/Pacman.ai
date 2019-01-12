import shelve

shelf = shelve.open("a")
print("HELOOO")
shelf["d"] = 12345
print("Stored")
shelf.close()
print("Closed")

shelf = shelve.open("a")
print("Opening again")
d = shelf["d"]
print(d)
#x = shelf["replay_buffer"]

shelf.close()
