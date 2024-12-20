# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

# from collections import defaultdict
from itertools import product
# from pprint import pprint

# filename: str = 'test.txt'
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


def manhattan_distance(p1: tuple, p2: tuple) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


# first, review the racetrack to find start & end
for x, y in product(range(MAX_X), range(MAX_Y)):
    if racetrack[y][x] == 'S':
        starting_point = (x, y)
    elif racetrack[y][x] == 'E':
        ending_point = (x, y)

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

full_path_length = len(path) - 1
print(f'Original racetrack is {full_path_length} moves long.')

# for each cheat, shortcut the path
# cheat_results = defaultdict(int)
good_count = 0
for i in range(len(path)-1):
    for j in range(i+1, len(path), 1):
        start_pos = path[i]
        end_pos = path[j]
        md = manhattan_distance(start_pos, end_pos)
        if md > 20:
            continue
        potential_cheat_shortcut = md - 2

        shortened_path = path[:i + 1] + path[j:]
        cheat_path_length = len(shortened_path) + potential_cheat_shortcut

        cheat_path_savings = full_path_length - cheat_path_length

        # print('-----')
        # pprint(path)
        # print(f'{i}: {start_pos}')
        # print(f'{j}: {end_pos}')
        # pprint(shortened_path)
        # print(cheat_path_length)
        # print(cheat_path_savings)

        # if cheat_path_savings >= 50:
        #     cheat_results[cheat_path_savings] += 1
        if cheat_path_savings >= 100:
            good_count += 1

# pprint(cheat_results)
print(good_count)
