from collections import defaultdict
from itertools import combinations, product

# filename: str = 'sample.txt'
filename: str = 'input.txt'

antenna_map = [line.rstrip() for line in open(filename).readlines()]
Y_MAX = len(antenna_map)
X_MAX = len(antenna_map[0])

antenna_locations = defaultdict(list)

for x, y in product(range(X_MAX), range(Y_MAX)):
    if antenna_map[y][x] != '.':
        antenna_locations[antenna_map[y][x]].append((x, y))

antinode_locations = set()
for antenna in antenna_locations:
    for first_antenna_pos, second_antenna_pos in combinations(antenna_locations[antenna], 2):
        dx = second_antenna_pos[0] - first_antenna_pos[0]
        dy = second_antenna_pos[1] - first_antenna_pos[1]

        nx1 = first_antenna_pos[0]
        ny1 = first_antenna_pos[1]

        while 0 <= nx1 < X_MAX and 0 <= ny1 < Y_MAX:
            antinode_locations.add((nx1, ny1))
            nx1 -= dx
            ny1 -= dy

        nx2 = second_antenna_pos[0]
        ny2 = second_antenna_pos[1]

        while 0 <= nx2 < X_MAX and 0 <= ny2 < Y_MAX:
            antinode_locations.add((nx2, ny2))
            nx2 += dx
            ny2 += dy

for y in range(Y_MAX):
    line = ''
    for x in range(X_MAX):
        if antenna_map[y][x] == '.' and (x, y) in antinode_locations:
            line += '#'
        else:
            line += antenna_map[y][x]
    print(line)

print(len(antinode_locations))
