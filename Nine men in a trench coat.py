#Nine men in a trench coat
from queue import PriorityQueue
import numpy as np
from copy import deepcopy
# Looks like this
#       _   _   _  
# _ _ _ _ _ _ _ _ _ _

class Node():
    def __init__(self,state,action,parent):
        if parent:
            self.cost = get_cost(state) + parent.cost
        else:
            self.cost = get_cost(state)
        self.state = state
        self.action = action
        self.parent = parent
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0

    def __lt__(self,rhs):
        if self.cost == rhs.cost:
            return self.depth < rhs.depth
        return self.cost < rhs.cost
    
    def __lte__(self,rhs):
        if self.cost == rhs.cost:
            return self.depth <= rhs.depth
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
    (-1,-1),(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8)
]
def get_cost(game_state):
    # if np.where(game_state == 1) != (1,0):
    #     soldier_range = range(1,2)
    # else:
    #     soldier_range = range(2,10)
    soldier_range = range(1,10)
    cost = 0
    for soldier in soldier_range:
        # soldiers 1->9
        soldier_loc = np.where(game_state == soldier)
        cost += int(abs((soldier_loc[0] - goal_locs[soldier][0])) + abs((soldier_loc[1] - goal_locs[soldier][1])))
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

    # set ranges for iterating to find soldiers
    # if soldier 1 is in place, leave him alone
    yrange = range(game_state.shape[0])
    if np.where(node.state == 1) == (1,0):
        xrange = range(game_state.shape[1][1:])
    else:
        xrange = range(game_state.shape[1])

    for i in yrange:
        for j in xrange:
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
    if iterations % 25_000 == 0:
        print(f"Iterations: {iterations}\nMax_Queue_Size: {max_queue_size}\nExpansions: {expansions}\n")
    # tracking
    iterations += 1
    max_queue_size = max(max_queue_size,pq.qsize())
    # get lowest cost node from p-queue
    node = pq.get()

    if iterations % 100_000 == 0:
      print(f"Best State So Far:\n\n{node.state}")

    # goal check
    if is_goal(node.state):
        print("Seargant is in place...")
        moves = []
        depth = node.depth
        while node.parent is not None:
            moves.append(node.action)
            node = node.parent
        moves.append(node.action)
        for move in moves[::-1]:
            print(f"{move}",end=" -> ")
        print(f"Max_Queue_Size: {max_queue_size}\nExpansions: {expansions}\nDepth: {depth}\n")
        quit()

    # expand current lowest code node
    expansions += 1
    new_nodes = expand(node)
    for new_node in new_nodes:
        pq.put(new_node)