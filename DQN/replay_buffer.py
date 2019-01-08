import collections

''' Stores transition tuples (s_t, a_t, r_t, s_t+1)'''
replay_buffer = collections.deque([])
td_error = collections.deque([])
P = collections.deque([])

count = 0
def pop_experience(index):
    global replay_buffer
    global td_error
    global P

    del replay_buffer[index]
    del td_error[index]
    del P[index]

def sort_buffer():
    global replay_buffer
    global td_error
    replay_buffer = [x for _,x in sorted(zip(td_error, replay_buffer))]
    td_error = collections.deque(sorted(td))

def calculate_probability(alpha): #use after replay_buffer is sorted according to td error.
    global P
    global replay_buffer
    global td_error

    sigma_p = 0

    for i in range(len(replay_buffer)):
        P.append(1/(i+1))
        sigma_p += (1/(i+1))**alpha

    for i in range(len(replay_buffer)):
        P[i] = (P[i]**alpha)/sigma_p
