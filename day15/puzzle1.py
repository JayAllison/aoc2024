from itertools import product
from pprint import pprint

# filename = 'sample1.txt'
# filename = 'sample2.txt'
filename = 'input.txt'


def display_warehouse(title: str):
    print(title)
    for row in warehouse_map:
        print(''.join(row))
    print()


map_lines, moves_lines = open(filename).read().split('\n\n')
warehouse_map = [[c for c in line.rstrip()] for line in map_lines.split('\n')]
MAX_Y = len(warehouse_map)
MAX_X = len(warehouse_map[0])
movements = moves_lines.replace('\n', '')

moves = {
    '^': (0, -1),
    '>': (+1, 0),
    'v': (0, +1),
    '<': (-1, 0),
}

robot_location = (-1, -1)
for x, y in product(range(MAX_X), range(MAX_Y)):
    if warehouse_map[y][x] == '@':
        robot_location = (x, y)
        break

# display_warehouse('Initial state:')

for movement in movements:
    rx, ry = robot_location
    mx, my = moves[movement]

    # print(f'From ({rx}, {ry}) moving {movement}')
    nx, ny = rx, ry
    path = [(nx, ny)]
    while True:
        nx, ny = nx + mx, ny + my
        path.append((nx, ny))
        if warehouse_map[ny][nx] == '#':
            # print(f'robot at ({rx}, {ry}), wall at ({nx}, {ny})')
            break
        elif warehouse_map[ny][nx] == '.':
            # print(f'robot at ({rx}, {ry}), open space at ({nx}, {ny}), need {len(path)-1} moves')
            path.reverse()
            for i in range(len(path)-1):
                dst_x, dst_y = path[i]
                src_x, src_y = path[i+1]
                # print(f'Moving {warehouse_map[src_y][src_x]} from ({src_x}, {src_y}) to ({dst_x}, {dst_y})')
                warehouse_map[dst_y][dst_x] = warehouse_map[src_y][src_x]
            warehouse_map[ry][rx] = '.'
            robot_location = path[-2]
            break

    # display_warehouse(f'Move {movement}')

coordinates = [y * 100 + x for x, y in product(range(MAX_X), range(MAX_Y)) if warehouse_map[y][x] == 'O']
print(sum(coordinates))
