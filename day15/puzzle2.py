from itertools import product

# filename = 'sample2.txt'
# filename = 'sample3.txt'
# filename = 'tests.txt'
filename = 'input.txt'

DEBUG: bool = False


def dprint(debug_string):
    if DEBUG:
        print(debug_string)


def display_warehouse(title: str):
    if DEBUG:
        print(title)
        for row in warehouse_map:
            print(''.join(row))
        print()


map_lines, moves_lines = open(filename).read().split('\n\n')
warehouse_map: list = []
for line in map_lines.split('\n'):
    new_row: list = []
    for c in line.rstrip():
        if c == '#':
            new_row.extend('##')
        elif c == 'O':
            new_row.extend('[]')
        elif c == '@':
            new_row.extend('@.')
        elif c == '.':
            new_row.extend('..')
        else:
            dprint('this should not happen')
    warehouse_map.append(new_row)

MAX_Y: int = len(warehouse_map)
MAX_X: int = len(warehouse_map[0])

movements: str = moves_lines.replace('\n', '')

moves: dict[str, tuple] = {
    '^': (0, -1),
    '>': (+1, 0),
    'v': (0, +1),
    '<': (-1, 0),
}

robot_location: tuple = (-1, -1)
for x, y in product(range(MAX_X), range(MAX_Y)):
    if warehouse_map[y][x] == '@':
        robot_location = (x, y)
        break

display_warehouse(f'Initial state [robot at ({robot_location[0]}, {robot_location[1]})]:')

mcount: int = 0
for movement in movements:
    mcount += 1
    rx, ry = robot_location
    mx, my = moves[movement]
    if movement in ('<', '>'):
        # re-use Part 1 for horizontal movement
        dprint(f'From ({rx}, {ry}) moving {movement}')
        nx, ny = rx, ry
        path: list[tuple] = [(nx, ny)]
        while True:
            nx, ny = nx + mx, ny + my
            path.append((nx, ny))
            if warehouse_map[ny][nx] == '#':
                dprint(f'robot at ({rx}, {ry}), wall at ({nx}, {ny})')
                break
            elif warehouse_map[ny][nx] == '.':
                dprint(f'robot at ({rx}, {ry}), open space at ({nx}, {ny}), need {len(path)-1} moves')
                path.reverse()
                for i in range(len(path)-1):
                    dst_x, dst_y = path[i]
                    src_x, src_y = path[i+1]
                    dprint(f'Moving {warehouse_map[src_y][src_x]} from ({src_x}, {src_y}) to ({dst_x}, {dst_y})')
                    warehouse_map[dst_y][dst_x] = warehouse_map[src_y][src_x]
                warehouse_map[ry][rx] = '.'
                robot_location = path[-2]
                break
    else:
        # Part 2: vertical movement
        nx, ny = rx, ry
        paths: list[list[tuple]] = [[(nx, ny)]]
        found_wall: bool = False
        all_clear: bool = False

        while not found_wall and not all_clear:
            new_paths: list = []
            clear_count: int = 0
            dprint(f'Checking {len(paths)} paths')
            for path in paths:
                new_paths.append(path)
                px, py = path[-1]
                nx, ny = px + mx, py + my
                path.append((nx, ny))
                if warehouse_map[ny][nx] == '#':
                    dprint(f'robot at ({rx}, {ry}), wall at ({nx}, {ny})')
                    found_wall = True
                elif warehouse_map[ny][nx] == '[' and warehouse_map[py][px] != '[':
                    dprint(f'robot at ({rx}, {ry}), left side of box at ({nx}, {ny})')
                    new_paths.append([(nx+1, ny)])
                elif warehouse_map[ny][nx] == ']' and warehouse_map[py][px] != ']':
                    dprint(f'robot at ({rx}, {ry}), right side of box at ({nx}, {ny})')
                    new_paths.append([(nx-1, ny)])
                elif warehouse_map[ny][nx] == '.':
                    dprint(f'robot at ({rx}, {ry}), an open space at ({nx}, {ny})')
                    # work-around: this path ends here, but other paths may go deeper
                    # let this blank spot keep getting found each iteration until all paths have found a blank spot
                    path.pop()
                    clear_count += 1

            if clear_count == len(paths):
                dprint('All clear to move')
                all_clear = True
                # work-around: not every path is the same length - add on the final blank spot here
                for path in paths:
                    px, py = path[-1]
                    nx, ny = px + mx, py + my
                    path.append((nx, ny))

            paths = new_paths

        # move each column the appropriate number of places
        if found_wall:
            dprint('Wall blocking move.')
        elif all_clear:
            for path in paths:
                path.reverse()
                for i in range(len(path)-1):
                    dst_x, dst_y = path[i]
                    src_x, src_y = path[i+1]
                    dprint(f'Moving {warehouse_map[src_y][src_x]} from ({src_x}, {src_y}) to ({dst_x}, {dst_y})')
                    warehouse_map[dst_y][dst_x] = warehouse_map[src_y][src_x]
                ox, oy = path[-1]
                warehouse_map[oy][ox] = '.'

            robot_location = rx + mx, ry + my
            dprint(f'robot moved to ({robot_location[0]}, {robot_location[1]})')

    display_warehouse(f'Move {movement} ({mcount})')

coordinates = [y * 100 + x for x, y in product(range(MAX_X), range(MAX_Y)) if warehouse_map[y][x] == '[']
print(sum(coordinates))
