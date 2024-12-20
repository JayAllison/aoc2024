# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

from collections import defaultdict
from itertools import product

# filename: str = 'sample.txt'
filename: str = 'input.txt'

# parse the input points into a list
racetrack: list[str] = [line.rstrip() for line in open(filename).readlines()]
MAX_Y = len(racetrack)
MAX_X = len(racetrack[0])

starting_point: tuple = (0, 0)
ending_point: tuple = (MAX_X, MAX_Y)

N: tuple = (0, -1)
E: tuple = (+1, 0)
S: tuple = (0, +1)
W: tuple = (-1, 0)

# a list of directional movements, so we can easily iterate over it
DIRECTIONS: list[tuple] = [N, E, S, W]


def add_points(p1: tuple, p2: tuple) -> tuple:
    return p1[0] + p2[0], p1[1] + p2[1]


# first, review the racetrack to find start, end, and Part 1's type of cheat possibilities
# we don't know yet which direction the cheat flows, but we can figure that out in a bit
cheat_possibilities: list[list[tuple]] = []
for x, y in product(range(MAX_X), range(MAX_Y)):
    if racetrack[y][x] == 'S':
        starting_point = (x, y)
    elif racetrack[y][x] == 'E':
        ending_point = (x, y)
    elif racetrack[y][x] == '#':
        # TODO: refactor?
        ux, uy = add_points((x, y), N)
        dx, dy = add_points((x, y), S)
        lx, ly = add_points((x, y), W)
        rx, ry = add_points((x, y), E)

        if 0 <= ux < MAX_X and 0 <= uy < MAX_Y and 0 <= dx < MAX_X and 0 <= dy < MAX_Y:
            if racetrack[uy][ux] in '.SE' and racetrack[dy][dx] in '.SE':
                cheat_possibilities.append([(ux, uy), (x, y), (dx, dy)])

        if 0 <= lx < MAX_X and 0 <= ly < MAX_Y and 0 <= rx < MAX_X and 0 <= ry < MAX_Y:
            if racetrack[ly][lx] in '.SE' and racetrack[ry][rx] in '.SE':
                cheat_possibilities.append([(lx, ly), (x, y), (rx, ry)])

# now that we know start & end, let's trace out the path
path: list[tuple] = [starting_point]
current = starting_point
while path[-1] != ending_point:
    for d in DIRECTIONS:
        possible = add_points(current, d)
        if racetrack[possible[1]][possible[0]] in '.E' and possible not in path:
            path.append(possible)
            current = possible
            break

full_path_score = len(path) - 1
print(f'Original racetrack is {full_path_score} moves long.')
print(f'Found {len(cheat_possibilities)} possible cheat paths.')

# for each cheat, shortcut the path
# cheat_results = defaultdict(int)
good_count = 0
for cheat_path in cheat_possibilities:
    index1 = path.index(cheat_path[0])
    index2 = path.index(cheat_path[2])

    if index1 < index2:
        shortened_path = path[:index1+1] + path[index2:]
    else:
        shortened_path = path[:index2+1] + path[index1:]

    cheat_path_length = full_path_score - len(shortened_path)
    # cheat_results[cheat_path_length] += 1
    if cheat_path_length >= 100:
        good_count += 1


# pprint(cheat_results)
print(good_count)
