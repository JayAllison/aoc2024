from collections import defaultdict
from itertools import product
from sys import maxsize

# filename: str = 'sample.txt'; MAX_X = 6; MAX_Y = 6; simulated_steps = 12
filename: str = 'input.txt'; MAX_X = 70; MAX_Y = 70; simulated_steps = 1024

# parse the input points into a list
incoming_bytes: list[tuple] = [tuple(int(c) for c in line.rstrip().split(',')) for line in open(filename).readlines()]

# today's puzzle explicitly defines the starting and ending points
start: tuple = (0, 0)  # start in top left
end: tuple = (MAX_X, MAX_Y)  # end in bottom right

N: tuple = (0, -1)
E: tuple = (+1, 0)
S: tuple = (0, +1)
W: tuple = (-1, 0)

# a list of directional movements, so we can easily iterate over it
DIRECTIONS: list[tuple] = [N, E, S, W]


# for Part 2, we need to run Dijkstra multiple times, so make it a utility function
def find_path(simulated_count: int) -> int | None:
    # https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    # Dijkstra #1: Create a set of all unvisited nodes
    corruptions = incoming_bytes[:simulated_count]
    unvisited_nodes: list[tuple] = [(x, y) for x, y in product(range(MAX_X+1), range(MAX_Y+1))
                                    if (x, y) not in corruptions]

    # Dijkstra #2: Assign to every node a distance from start value:
    # for the starting node, it is zero, and for all other nodes, it is infinity
    scores: defaultdict[tuple: int] = defaultdict(lambda: maxsize)
    scores[start] = 0

    # Dijkstra 3a: If the unvisited set is empty, then the algorithm terminates
    while unvisited_nodes:
        # Dijkstra #3b: From the unvisited set, select the current node to be one with the smallest (finite) distance
        # using sorted() to sort unvisited locations by score (lowest to highest) and then take the first one
        current_node = sorted(unvisited_nodes, key=lambda p: scores[p])[0]
        current_score = scores[current_node]

        # Dijkstra #3c: the algorithm terminates once the current node is the target node (if it happens)
        if current_node == end:
            return scores[current_node]

        # Dijkstra 3a: If the unvisited set contains only nodes with infinite distance
        # (which are unreachable), then the algorithm terminates
        # for Part 2, we do not know if there is a solution, so we need to account for not finding a suitable path
        if current_score == maxsize:
            return None

        # Dijkstra #4a: For the current node, consider all of its unvisited neighbors
        # and update their distances through the current node
        for direction in DIRECTIONS:
            neighbor: tuple = (current_node[0] + direction[0], current_node[1] + direction[1])
            neighbor_score: int = current_score + 1

            # Dijkstra #4b: compare the newly calculated distance to the one currently
            # assigned to the neighbor and assign the smaller one to it
            if neighbor in unvisited_nodes and neighbor_score < scores[neighbor]:
                scores[neighbor] = neighbor_score

        # Dijkstra #5: the current node is removed from the unvisited set
        unvisited_nodes.remove(current_node)

    return None


# use a binary search to avoid having to test every possible value
# https://en.wikipedia.org/wiki/Binary_search
left = 0
right = len(incoming_bytes) - 1

while left < right:
    middle = (left + right) // 2
    if path_length := find_path(middle):
        left = middle
        print(f'Path found at {middle}')
        if left + 1 == right:
            print(f'Exit prevented by {incoming_bytes[left]}')
            break
    else:
        right = middle
        print(f'Path not found at {middle}')
        if left + 1 == right:
            print(f'Exit prevented by {incoming_bytes[left]}')
            break
