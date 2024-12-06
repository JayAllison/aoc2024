import itertools

# filename = "sample.txt"
filename = "input.txt"

lab_map = [line for line in open(filename)]
y_max = len(lab_map)
x_max = len(lab_map[0])


def is_within_map(point) -> bool:
    return 0 <= point[0] < x_max and 0 <= point[1] < y_max


directions = ['N', 'E', 'S', 'W']

moves = {
    'N': (+0, -1),
    'E': (+1, +0),
    'S': (+0, +1),
    'W': (-1, +0)
}

visited = set()
current_pos = (-1, -1)
current_dir = 0

for x, y in itertools.product(range(x_max), range(y_max)):
    if lab_map[y][x] == '^':
        current_pos = (x, y)
        break

while is_within_map(current_pos):
    visited.add(current_pos)
    nx, ny = (current_pos[0] + moves[directions[current_dir]][0], current_pos[1] + moves[directions[current_dir]][1])
    if is_within_map((nx, ny)) and lab_map[ny][nx] == '#':
        current_dir = (current_dir + 1) % len(directions)
    else:
        current_pos = (nx, ny)

print(len(visited))
