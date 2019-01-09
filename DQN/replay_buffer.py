import collections

''' Stores transition tuples (s_t, a_t, r_t, s_t+1)'''
replay_buffer = []
replay_buffer_two = []
#td_error = collections.deque([])
P = []
P_two = []

count = 0
count_two = 0

def pop_experience(index, buffer):
    global replay_buffer
    global replay_buffer_two
    #global td_error
    global P
    global P_two

    if buffer == 2:
        del(replay_buffer_two[index])
        del(P_two[index])

    elif buffer == 1:
        del(replay_buffer[index])
        del(P[index])

#def sort_buffer():
    #global replay_buffer
    #global td_error
    #replay_buffer = [x for _,x in sorted(zip(td_error, replay_buffer))]
    #td_error = collections.deque(sorted(td))

def calculate_probability(alpha, buffer): #use after replay_buffer is sorted according to td error.
    global P
    global P_two
    global replay_buffer
    global replay_buffer_two
    #global td_error

    sigma_p = 0
    if buffer == 1:
        for i in range(len(replay_buffer)):
            P.append(1/(i+1))
            sigma_p += (1/(i+1))**alpha

        for i in range(len(replay_buffer)):
            P[i] = (P[i]**alpha)/sigma_p

    elif buffer == 2:
        for i in range(len(replay_buffer_two)):
            P_two.append(1/(i+1))
            sigma_p += (1/(i+1))**alpha

        for i in range(len(replay_buffer_two)):
            P_two[i] = (P_two[i]**alpha)/sigma_p
