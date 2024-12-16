from collections import defaultdict
from itertools import product
from sys import maxsize

# filename: str = 'sample.txt'
# filename: str = 'sample2.txt'
filename: str = 'input.txt'

# parse the input into a 2D grid, then find the bounds of that grid
maze: list[str] = [line.rstrip() for line in open(filename).readlines()]
MAX_Y: int = len(maze)
MAX_X: int = len(maze[0])

# we could search for these, but since the location is specified by the puzzle, we don't have to
start: tuple = (1, len(maze)-2)  # start in bottom left
end: tuple = (len(maze[0])-2, 1)  # end in top right

# delta movements for each direction
NULL: tuple = (0, 0)  # for the defaultdict default value only
N: tuple = (0, -1)
E: tuple = (+1, 0)
S: tuple = (0, +1)
W: tuple = (-1, 0)

# the sequence of directional movements, in clockwise order
CW_ROTATION: list[tuple] = [N, E, S, W]
DIR_LEN: int = len(CW_ROTATION)

# the relative cost of moving clockwise from the current direction
ROTATION_COST: list[int] = [0, 1000, 2000, 1000]

# https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
# Dijkstra #1: Create a set of all unvisited nodes
unvisited_nodes: list[tuple] = [(x, y) for x, y in product(range(MAX_X), range(MAX_Y)) if maze[y][x] in '.SE']

# Dijkstra #2: Assign to every node a distance from start value:
# for the starting node, it is zero, and for all other nodes, it is infinity
# in addition to normal Dijkstra, our puzzle requires that we track the direction of travel that generated this score
scores: defaultdict[tuple: tuple] = defaultdict(lambda: (maxsize, NULL))

# start facing East
scores[start] = (0, E)

while True:
    # Dijkstra #3a: From the unvisited set, select the current node to be the one with the smallest (finite) distance
    # using sorted() to sort unvisited locations by score (lowest to highest) and then take the first one
    # for our puzzle, direction does not factor in here - just score
    current_node = sorted(unvisited_nodes, key=lambda p: scores[p][0])[0]
    current_score, current_direction = scores[current_node]

    # Dijkstra #3b: the algorithm terminates once the current node is the target node
    if current_node == end:
        print(scores[current_node][0])
        break

    # Dijkstra #4a: For the current node, consider all of its unvisited neighbors
    # and update their distances through the current node
    direction_index: int = CW_ROTATION.index(current_direction)

    # check each direction in clockwise order from the current direction,
    # starting with straight ahead and then rotating clockwise three times
    for i in range(DIR_LEN):
        # which direction we're about to move in
        new_direction: tuple = CW_ROTATION[(direction_index + i) % DIR_LEN]
        # what the position of that new location is
        neighbor: tuple = (current_node[0] + new_direction[0], current_node[1] + new_direction[1])
        # what the cost of that move is, based on how much we had to rotate (if any)
        neighbor_score: int = current_score + ROTATION_COST[i] + 1

        # Dijkstra #4b: compare the newly calculated distance to the one currently
        # assigned to the neighbor and assign the smaller one to it
        # for our puzzle, direction does not factor into the comparison - just score
        if neighbor in unvisited_nodes and neighbor_score < scores[neighbor][0]:
            # but direction does matter now - we must store the direction with the score,
            # so we know what direction we were moving to get this low score
            scores[neighbor] = (neighbor_score, new_direction)

    # Dijkstra #5: the current node is removed from the unvisited set
    unvisited_nodes.remove(current_node)
