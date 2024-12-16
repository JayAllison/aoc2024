from itertools import product

filename = 'sample2.txt'
# filename = 'sample3.txt'
# filename = 'tests.txt'
# filename = 'input.txt'

# set to True to enble debug print statements
DEBUG: bool = False
# DEBUG: bool = True


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

# expand the original input into the horizontally-doubled input, per the Part 2 instructions
for line in map_lines.split('\n'):
    # expand each row
    new_row: list = []
    for original_character in line.rstrip():
        if original_character == '#':
            new_row.extend('##')
        elif original_character == 'O':
            new_row.extend('[]')
        elif original_character == '@':
            new_row.extend('@.')
        elif original_character == '.':
            new_row.extend('..')
    # save this expanded row
    warehouse_map.append(new_row)

# how big our expanded map is
MAX_Y: int = len(warehouse_map)
MAX_X: int = len(warehouse_map[0])

# Day 15 instructions say "newlines within the move sequence should be ignored"
movements: str = moves_lines.replace('\n', '')

# the x, y delta that corresponds to each movement instruction
moves: dict[str, tuple] = {
    '^': (0, -1),
    '>': (+1, 0),
    'v': (0, +1),
    '<': (-1, 0),
}

# find the robot's starting position
# (providing an initial value just to clear up IDE warnings)
robot_location: tuple = (-1, -1)
for x, y in product(range(MAX_X), range(MAX_Y)):
    if warehouse_map[y][x] == '@':
        robot_location = (x, y)
        break

display_warehouse(f'Initial state [robot at ({robot_location[0]}, {robot_location[1]})]:')

mcount: int = 0  # useful when debugging to know which move we're on

# exercise each move instruction, using the Part 2 rules
for movement in movements:
    mcount += 1
    robot_starting_x, robot_starting_y = robot_location
    move_delta_x, move_delta_y = moves[movement]

    if movement in ('<', '>'):
        # re-use Part 1 for horizontal movement
        dprint(f'From ({robot_starting_x}, {robot_starting_y}) moving {movement}')
        next_x, next_y = robot_starting_x, robot_starting_y

        # keep track of all of the things that need to move
        path: list[tuple] = [(next_x, next_y)]

        while True:
            next_x, next_y = next_x + move_delta_x, next_y + move_delta_y
            # add this position to the list of things that need to move
            path.append((next_x, next_y))

            # if we reach a wall, then no movement needs to happen - break out of this while loop, go to next movement
            if warehouse_map[next_y][next_x] == '#':
                dprint(f'robot at ({robot_starting_x}, {robot_starting_y}), wall at ({next_x}, {next_y})')
                break
            # if we find an open spot, we are ready to move
            elif warehouse_map[next_y][next_x] == '.':
                dprint(f'robot at ({robot_starting_x}, {robot_starting_y}), '
                       f'open space at ({next_x}, {next_y}), need {len(path) - 1} moves')
                # we are going to move the things from last to first
                path.reverse()
                for i in range(len(path)-1):
                    dst_x, dst_y = path[i]
                    src_x, src_y = path[i+1]
                    dprint(f'Moving {warehouse_map[src_y][src_x]} from ({src_x}, {src_y}) to ({dst_x}, {dst_y})')
                    warehouse_map[dst_y][dst_x] = warehouse_map[src_y][src_x]

                # overwrite the original location with empty space
                warehouse_map[robot_starting_y][robot_starting_x] = '.'

                # move our marker for the robot (yes, we already moved the @,
                # but I don't use that again after finding it the first time)
                robot_location = robot_starting_x + move_delta_x, robot_starting_y + move_delta_y

                # move onto the next movement
                break
    else:
        # Part 2: vertical movement - similar to Part 1, but overlapping boxes can cause movement in multiple columns
        next_x, next_y = robot_starting_x, robot_starting_y

        # we may need to move multiple parallel columns - keep track of all lof them
        paths: list[list[tuple]] = [[(next_x, next_y)]]
        found_wall: bool = False
        all_clear: bool = False

        # keep going until we either hit a wall or can move everything forward
        while not found_wall and not all_clear:
            # we don't need to iterate over the same list we're modifying - make a new copy for the next iteration
            new_paths: list = []

            # keep track of how many columns are clear to move
            clear_count: int = 0

            # for each column, check the next step
            dprint(f'Checking {len(paths)} paths')
            for path in paths:
                new_paths.append(path)
                current_x, current_y = path[-1]
                next_x, next_y = current_x + move_delta_x, current_y + move_delta_y

                # add this position to the list of things that need to move
                path.append((next_x, next_y))

                # if we reach a wall, then no movement needs to happen - break out of this while loop, go to next move
                if warehouse_map[next_y][next_x] == '#':
                    dprint(f'robot at ({robot_starting_x}, {robot_starting_y}), wall at ({next_x}, {next_y})')
                    found_wall = True
                # if the next spot is occupied by a box that extends into a new column, start tracking that column, too
                elif warehouse_map[next_y][next_x] == '[' and warehouse_map[current_y][current_x] != '[':
                    dprint(f'robot at ({robot_starting_x}, {robot_starting_y}), '
                           f'left side of box at ({next_x}, {next_y})')
                    new_paths.append([(next_x + 1, next_y)])
                elif warehouse_map[next_y][next_x] == ']' and warehouse_map[current_y][current_x] != ']':
                    dprint(f'robot at ({robot_starting_x}, {robot_starting_y}), '
                           f'right side of box at ({next_x}, {next_y})')
                    new_paths.append([(next_x - 1, next_y)])
                # if we find an open spot, we are ready to move this column
                elif warehouse_map[next_y][next_x] == '.':
                    dprint(f'robot at ({robot_starting_x}, {robot_starting_y}), an open space at ({next_x}, {next_y})')
                    # work-around: this path ends here, but other paths may go deeper
                    # let this blank spot keep getting found each iteration until all paths have found a blank spot,
                    # even though some paths may extend further up (or down) than others
                    path.pop()
                    clear_count += 1

            # if every column has found an empty spot to move into, then get raeady to move them all
            if clear_count == len(paths):
                dprint('All clear to move')
                all_clear = True
                # work-around: not every path is the same length - add on the final blank spot here
                for path in paths:
                    current_x, current_y = path[-1]
                    next_x, next_y = current_x + move_delta_x, current_y + move_delta_y
                    path.append((next_x, next_y))

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

                # overwrite the original location with empty space
                original_x, original_y = path[-1]
                warehouse_map[original_y][original_x] = '.'

            # move our marker for the robot (yes, we already moved the @,
            # but I don't use that again after finding it the first time)
            robot_location = robot_starting_x + move_delta_x, robot_starting_y + move_delta_y
            dprint(f'robot moved to ({robot_location[0]}, {robot_location[1]})')

    display_warehouse(f'Move {movement} ({mcount})')

# calculate the GPS coordinates according to the puzzle rules
coordinates = [y * 100 + x for x, y in product(range(MAX_X), range(MAX_Y)) if warehouse_map[y][x] == '[']
print(sum(coordinates))
