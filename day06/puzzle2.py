from copy import deepcopy
from datetime import datetime
import itertools
# from pprint import pprint

start = datetime.now()
print(f'Starting at {start}')

# filename = "sample.txt"
filename = "input.txt"

lab_map = [list(line.rstrip()) for line in open(filename).readlines()]
y_max = len(lab_map)
x_max = len(lab_map[0])


def is_within_map(point) -> bool:
    return 0 <= point[0] < x_max and 0 <= point[1] < y_max


def try_to_traverse_map(modified_map, starting_pos):
    directions = ['N', 'E', 'S', 'W']

    moves = {
        'N': (+0, -1),
        'E': (+1, +0),
        'S': (+0, +1),
        'W': (-1, +0)
    }

    visited = set()
    previous_visit_size = 0
    stuck_count = 1000
    current_pos = starting_pos
    current_dir = 0

    while is_within_map(current_pos):
        visited.add(current_pos)

        # brute force, before I try to do anything clever - just see if I can detect a loop by not going anywhere new
        if len(visited) == previous_visit_size:
            stuck_count -= 1
            if stuck_count == 0:
                return 0
        previous_visit_size = len(visited)

        nx, ny = (current_pos[0] + moves[directions[current_dir]][0], current_pos[1] + moves[directions[current_dir]][1])
        if is_within_map((nx, ny)) and modified_map[ny][nx] == '#':
            current_dir = (current_dir + 1) % len(directions)
        else:
            current_pos = (nx, ny)

    return len(visited)


def copy_and_modify_map(point):
    mod_map = deepcopy(lab_map)
    mod_map[point[1]][point[0]] = '#'
    return mod_map


starting_position = (-1, -1)
non_obstacle_positions = []
for x, y in itertools.product(range(x_max), range(y_max)):
    if lab_map[y][x] == '^':
        starting_position = (x, y)
    elif lab_map[y][x] != '#':
        non_obstacle_positions.append((x, y))

count = 0
# brute force solution: try blocking every position to see if it causes a problem
for pos in non_obstacle_positions:
    new_map = copy_and_modify_map(pos)
    if not try_to_traverse_map(new_map, starting_position):
        count += 1
        print('.', end='', flush=True)
        if count % 100 == 0:
            print()

print()
print(f'Completed after {datetime.now() - start}')
print(count)
