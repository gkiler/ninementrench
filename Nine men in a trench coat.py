#Nine men in a trench coat
from queue import PriorityQueue
import numpy as np
from copy import deepcopy
# Looks like this
#       _   _   _  
# _ _ _ _ _ _ _ _ _ _

seen_states = set()

goal_state = np.array([
    [-1,-1,-1,0,-1,0,-1,0,-1,-1],
    [1,2,3,4,5,6,7,8,9,0]
])

def state_swap(old_state,first,second):
    game_state = deepcopy(old_state)
    game_state[first], game_state[second] = game_state[second], game_state[first]
    return game_state

def see_state(game_state):
    seen_states.add(game_state.to_bytes())

def get_cost(game_state):
    loc = np.where(game_state == 1)
    return loc[0] + loc[1]

def get_possible_operators(game_state):
    # iterate over each space
    # can the guy move up, down, left, or right?
    new_nodes = []
    for i in range(game_state.shape[0]):
        for j in range(game_state.shape[1]):
            if game_state[i,j] > 0:
                
                moves = [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]
                for move in moves:
                    if game_state[move] == 0:
                        new_state = state_swap(game_state,(i,j),move)
                        if new_state not in seen_states:
                            new_nodes.append((new_state,f"{(i,j)} to {move}"))
    return new_nodes
                
# Start state is like
init_state = np.array([
    [-1,-1,-1,0,-1,0,-1,0,-1,-1],
    [0,2,3,4,5,6,7,8,9,1]
])
#-1 represents solid dirt, each number is a person, 0 is empty space
print(get_cost(init_state))
pq = PriorityQueue()

