import shelve

shelf = shelve.open("objects")

'''
shelf["scores"] = []
print("Success!")
'''

for i in shelf["scores"]:
    print(i)

shelf.close()
