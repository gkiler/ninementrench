#Nine men in a trench coat
from queue import PriorityQueue
import numpy as np
from copy import deepcopy

# State
# Looks like this
#       _   _   _  
# _ _ _ _ _ _ _ _ _ _

class Node():
    # Nodes are given a state representation, an action representation of the previous move for traceback,
    # parent node reference for traceback, and depth for record keeping purposes
    def __init__(self,state,action,parent):
        self.state = state
        self.action = action
        self.parent = parent
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0

        if parent:
            self.cost = get_cost(state) + parent.cost
        else:
            self.cost = get_cost(state)

    #comparison operators needed for priority queue to work
    def __lt__(self,rhs):
        if self.cost == rhs.cost:
            return self.depth < rhs.depth
        return self.cost < rhs.cost
    
    def __lte__(self,rhs):
        if self.cost == rhs.cost:
            return self.depth <= rhs.depth
        return self.cost <= rhs.cost


#seen states will be a hash table of states converted to bytes for space saving measures
seen_states = set()

# Create goal state with soldiers
goal_state = np.array([
    [-1,-1,-1,0,-1,0,-1,0,-1,-1],
    [1,2,3,4,5,6,7,8,9,0]
])

# Deep copy previous state, then use python swap heuristic to create a return the new state
def state_swap(old_state,first,second):
    game_state = deepcopy(old_state)
    game_state[first], game_state[second] = game_state[second], game_state[first]
    return game_state

# Just a bit of laziness to access where each soldier should be in the goal state
goal_locs = [
    (-1,-1),(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8)
]
# Get cost iterates over all soldiers, customizable by soldier "ID"s, takes manhattan distance of curr pos vs goal pos
def get_cost(game_state):
    soldier_range = [1,2,3,4,5,6,7,8,9]
    cost = 0
    for soldier in soldier_range:
        soldier_loc = np.where(game_state == soldier)
        cost += int(abs((soldier_loc[0] - goal_locs[soldier][0])) + abs((soldier_loc[1] - goal_locs[soldier][1])))
    return cost

    # cost = np.sum(np.equal(game_state,goal_state)) # Misplaced heuristic doesnt seem to work either
    # return cost

    loc = np.where(game_state == 1) 
    return loc[0] + loc[1] # Distance for seargant does not work. Needs manhattan

def is_goal(game_state):
    # Numpy function just returns true if two states are equal.
    return np.array_equal(game_state,goal_state)

def expand(node):
    # in simple terms:
    # iterate over each space, is it a soldier?
    # can the guy move up, down, left, or right?
    new_nodes = []
    game_state = node.state

    moves = []
    for y in range(0,game_state.shape[0]):
        for x in range(0,game_state.shape[1]):
            if game_state[y,x] > 0:
                # check left, right, up, down
                moves = []
                # to get maximum move distance,
                # find if gamestate coord + i is 0, continue, etc
                try:
                    if game_state[y+1,x] == 0:
                        moves.append((y+1,x))
                except:
                    pass
                try:
                    if game_state[y-1,x] == 0:
                        moves.append((y-1,x))
                except:
                    pass
                try:
                    i = 1
                    # find if one over is empty, then 
                    # if two over is empty, so on.
                    # when not empty, ignore
                    temp = (y,x)
                    anything = False
                    while True:
                        if game_state[y,x+i] == 0:
                            temp = (y,x+i)
                            i += 1
                            anything = True
                        else:
                            break
                    if anything:
                        moves.append(temp)
                except:
                    pass
                try:
                    i = 1
                    # find if one over is empty, then 
                    # if two over is empty, so on.
                    # when not empty, ignore
                    temp = (y,x)
                    anything = False
                    while True:
                        if game_state[y,x-i] == 0:
                            temp = (y,x-i)
                            i += 1
                            anything = True
                        else:
                            break
                    if anything:
                        moves.append(temp)
                except:
                    pass
                for move in moves:
                    new_state = state_swap(game_state,(y,x),move)
                    if new_state.tobytes() not in seen_states:
                        new_nodes.append(Node(new_state,f"{(y,x)} to {move}",node))
                        # seen_states.add(new_state.tobytes()) 
    return new_nodes

                
# Start state
init_state = np.array([
    [-1,-1,-1,0,-1,0,-1,0,-1,-1],
    [0,2,3,4,5,6,7,8,9,1]
])

#-1 represents solid dirt, each number is a person, 0 is empty space
pq = PriorityQueue()
init_node = Node(init_state,"BEGIN",None)
pq.put(init_node)

iterations = 0
expansions = 0
max_queue_size = 0
# Iterate until all possible nodes have been tried

choice = int(input("Enter 1 for default problem, 2 for custom configuration: "))
if choice == 2:
    soldier_list = input("Give the order of soldiers 1->9 in the trench at the start, separated by spaces:\n").split(" ")
    for i, soldier in enumerate(soldier_list):
        init_state[1][i+1] = int(soldier)

while not pq.empty():
    if expansions % 100_000 == 0:
        print(f"\nIterations: {iterations}\nMax_Queue_Size: {max_queue_size}\nExpansions: {expansions}\n")
    # tracking
    iterations += 1
    max_queue_size = max(max_queue_size,pq.qsize())
    # get lowest cost node from p-queue
    node = pq.get()
    while node.state.tobytes() in seen_states:
        node = pq.get()
        iterations += 1

    # if expansions % 100_000 == 0:
    #   print(f"Best State So Far:\n\n{node.state}")



    # goal check,
    if is_goal(node.state):
        print("Seargant is in place...")
        moves = []
        depth = node.depth
        while node.parent is not None:
            moves.append(node.state)
            node = node.parent
        moves.append(node.state)
        for move in moves[::-1]:
            print(f"{move}",end="\n\n")
        print(f"\nMax_Queue_Size: {max_queue_size}\nExpansions: {expansions}\nDepth: {depth}\n")
        quit()

    # expand current lowest code node
    expansions += 1
    new_nodes = expand(node)
    seen_states.add(node.state.tobytes())
    for new_node in new_nodes:
        pq.put(new_node)