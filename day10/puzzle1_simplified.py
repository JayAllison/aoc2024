# -----------------------------------------------------------------------------
# Day 10, Part 1
#
# After today, I am not going to rewrite the Part 1 solution - I'm just going to comment it well.
#
# There are a lot of 2D map puzzles so far this year, so this should seem very familiar.
#
# The topographic map indicates the height at each position using a scale from 0 (lowest) to 9 (highest).
# A trailhead is any position that starts one or more hiking trails - here, these positions will always
# have height 0. A trailhead's score is the number of 9-height positions reachable from that trailhead
# via a hiking trail.
#
# What is the sum of the scores of all trailheads on your topographic map?
#
# -----------------------------------------------------------------------------

from itertools import product

# filename: str = 'sample.txt'
filename: str = 'input.txt'

# parse the map into a list of lists of integers that we will treat like a 2D array -
# I found it easier to go ahead and convert the value of every coordinate to an integer now
# remember that the outer index is Y and the inner index is X, which is backwards from math class,
# so the point (x, y) is antenna_map[y][x]
topo_map: list[list[int]] = [[int(p) for p in line.rstrip()] for line in open(filename).readlines()]

# calculate the boundaries for this map - as with all of the 2D maps in AoC so far this year, this one is also square
# remember that the Pythonic convention is to put constant value in all caps
Y_MAX: int = len(topo_map)
X_MAX: int = len(topo_map[0])

# make a list of all of the trailheads by checking every point on the map for a value of 0
# this list comprehension is equivalent to, but more compact than, nested for loops with a conditional
trailheads: list = [(th_x, th_y) for th_x, th_y in product(range(X_MAX), range(Y_MAX)) if topo_map[th_y][th_x] == 0]

# what directions can we move in? making a list like this lets us use a loop below instead of duplicating code
# Hiking trails never include diagonal steps - only up, down, left, or right (from the perspective of the map).
directions: list = [(-1, 0), (+1, 0), (0, -1), (0, +1)]

# the puzzle solution - we will add to it as we go along
total: int = 0

# this is not a path-following algorithm (ie, depth-first search),
# it's a step-forward-in-parallel algorithm (more like a breadth-first search),
# but the paths are not maintained, so it's really not either
# instead, it's inspired by Dijkstra's algorithm - step forward in every direction

# starting from every trailhead, walk every possible path to see if we find a peak
for x, y in trailheads:

    # Part 1 requires us to only count how many peaks are reachable, not how many times we reach them,
    # so we need to keep track of the peaks we've been to, so we don't count them twice
    peaks_found: list = []

    # these are the nodes that we need to visit next - when this list is empty, we're done with this trailhead
    next_steps: list = [(x, y)]

    # start at the trailhead and see where we can go from there
    for step_x, step_y in next_steps:

        # for each location, check in every permitted direction to see if we can step that way
        # and stay within the puzzle rules
        for direction in directions:
            next_x, next_y = step_x + direction[0], step_y + direction[1]
            # is this a valid move?
            if 0 <= next_x < X_MAX and 0 <= next_y < Y_MAX and topo_map[next_y][next_x] == topo_map[step_y][step_x] + 1:
                # if this next step is valid AND it's a peak AND we haven't seen this peak yet, record this peak
                # but, if we have already seen this peak, then skip it
                if topo_map[next_y][next_x] == 9 and (next_x, next_y) not in peaks_found:
                    peaks_found.append((next_x, next_y))
                # if this next step is a valid move and not a peak, add it to the list of positions to consider
                else:
                    next_steps.append((next_x, next_y))

    # how many unique peaks did we reach from this trailhead?
    total += len(peaks_found)

# display the result
print(total)
