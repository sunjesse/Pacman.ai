import shelve

shelf = shelve.open("objects")

#shelf["scores"] = []
#print("Success!")


#for i in shelf["scores"]:
#    print(i)

print(shelf["q_network"].alpha)
print(shelf["target_network"].alpha)
#print(shelf["q_network"].weights_layer_1)
#print(shelf["q_network"].weights_layer_2)
#print(shelf["q_network"].weights_layer_3)
shelf.close()
