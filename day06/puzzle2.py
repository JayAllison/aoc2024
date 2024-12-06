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


def try_to_traverse_map(modified_map, starting_pos, get_points=False):
    directions = ['N', 'E', 'S', 'W']

    moves = {
        'N': (+0, -1),
        'E': (+1, +0),
        'S': (+0, +1),
        'W': (-1, +0)
    }

    # optimization attempt 2 - Francis & Taylor suggested tracking point + direction for loop detection
    visited = set()
    current_pos = starting_pos
    current_dir = 0

    while is_within_map(current_pos):
        vector = current_pos + (current_dir,)
        if vector in visited:
            return 0  # found a loop
        visited.add(vector)

        nx, ny = (current_pos[0] + moves[directions[current_dir]][0], current_pos[1] + moves[directions[current_dir]][1])
        if is_within_map((nx, ny)) and modified_map[ny][nx] == '#':
            current_dir = (current_dir + 1) % len(directions)
        else:
            current_pos = (nx, ny)

    if get_points:
        return set([(vx, vy) for vx, vy, vd in visited])
    else:
        return len(visited)


def copy_and_modify_map(point):
    mod_map = deepcopy(lab_map)
    mod_map[point[1]][point[0]] = '#'
    return mod_map


starting_position = (-1, -1)
for x, y in itertools.product(range(x_max), range(y_max)):
    if lab_map[y][x] == '^':
        starting_position = (x, y)

# optimization attempt 1 - Francis suggested only check blocking places along the original path, excluding the start
non_obstacle_positions = try_to_traverse_map(lab_map, starting_position, get_points=True)
non_obstacle_positions.remove(starting_position)

count = 0
for pos in non_obstacle_positions:
    new_map = copy_and_modify_map(pos)
    if not try_to_traverse_map(new_map, starting_position):
        count += 1
        # print('.', end='', flush=True)
        # if count % 100 == 0:
        #     print()

print()
print(f'Completed after {datetime.now() - start}')
print(count)
