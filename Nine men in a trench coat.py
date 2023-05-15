#Nine men in a trench coat
from queue import PriorityQueue
import numpy as np
from copy import deepcopy
# Looks like this
#       _   _   _  
# _ _ _ _ _ _ _ _ _ _

class Node():
    def __init__(self,state,action,parent):
        self.cost = get_cost(state)
        self.state = state
        self.action = action
        self.parent = parent

    def __lt__(self,rhs):
        return self.cost < rhs.cost
    
    def __lte__(self,rhs):
        return self.cost <= rhs.cost


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

goal_locs = [
    (-1,-1),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9)
]
def get_cost(game_state):
    cost = 0
    for soldier in range(1,10):
        # soldiers 1->9
        soldier_loc = np.where(soldier==game_state,game_state)
        cost += abs((soldier_loc[0] - goal_locs[soldier][0])) + abs((soldier_loc[1] - goal_locs[soldier][1]))
    return cost

    cost = np.sum(np.equal(game_state,goal_state)) # Misplaced heuristic doesnt seem to work either
    return cost

    loc = np.where(game_state == 1) 
    return loc[0] + loc[1] # Distance for seargant does not work. Needs manhattan

def is_goal(game_state):
    return np.array_equal(game_state,goal_state)

def expand(node):
    # iterate over each space
    # can the guy move up, down, left, or right?
    new_nodes = []
    game_state = node.state
    for i in range(game_state.shape[0]):
        for j in range(game_state.shape[1]):
            if game_state[i,j] > 0:
                moves = [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]
                for move in moves:
                    try:
                        if game_state[move] == 0:
                            pass
                    except:
                        continue
                    if game_state[move] == 0:
                        new_state = state_swap(game_state,(i,j),move)
                        if new_state.tobytes() not in seen_states:
                            new_nodes.append(Node(new_state,f"{(i,j)} to {move}",node))
                            seen_states.add(new_state.tobytes()) 
    return new_nodes

                
# Start state is like
init_state = np.array([
    [-1,-1,-1,0,-1,0,-1,0,-1,-1],
    [0,2,3,4,5,6,7,8,9,1]
])
#-1 represents solid dirt, each number is a person, 0 is empty space
print(get_cost(init_state))
pq = PriorityQueue()
init_node = Node(init_state,"BEGIN",None)
pq.put(init_node)

iterations = 0
expansions = 0
max_queue_size = 0
while not pq.empty():
    if iterations % 1000 == 0:
        print(f"Iterations: {iterations}\nMax_Queue_Size: {max_queue_size}\nExpansions: {expansions}\n")
    # tracking
    iterations += 1
    max_queue_size = max(max_queue_size,pq.qsize())
    # get lowest cost node from p-queue
    node = pq.get()

    # goal check
    if is_goal(node.state):
        print("Seargant is in place...")
        moves = []
        while node.parent is not None:
            moves.append(node.action)
            node = node.parent
        moves.append(node.action)
        for move in moves[::-1]:
            print(f"{move}",end=" -> ")

    # expand current lowest code node
    expansions += 1
    new_nodes = expand(node)
    for new_node in new_nodes:
        pq.put(new_node)