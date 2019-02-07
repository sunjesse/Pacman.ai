def ema(previous, beta, data_point):
    return beta*previous - (1-beta)*data_point
    
