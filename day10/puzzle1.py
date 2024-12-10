
from itertools import product

# filename: str = 'sample.txt'
filename: str = 'input.txt'

topo_map: list[list[int]] = [[int(p) for p in line.rstrip()] for line in open(filename).readlines()]
Y_MAX: int = len(topo_map)
X_MAX: int = len(topo_map[0])

trailheads: list = [(th_x, th_y) for th_x, th_y in product(range(X_MAX), range(Y_MAX)) if topo_map[th_y][th_x] == 0]
directions: list = [(-1, 0), (+1, 0), (0, -1), (0, +1)]
total: int = 0

for x, y in trailheads:
    peaks_found: list = []
    next_steps: list = [(x, y)]
    for step_x, step_y in next_steps:
        for direction in directions:
            next_x, next_y = step_x + direction[0], step_y + direction[1]
            if 0 <= next_x < X_MAX and 0 <= next_y < Y_MAX and topo_map[next_y][next_x] == topo_map[step_y][step_x] + 1:
                if topo_map[next_y][next_x] == 9 and (next_x, next_y) not in peaks_found:
                    peaks_found.append((next_x, next_y))
                else:
                    next_steps.append((next_x, next_y))
    total += len(peaks_found)

print(total)
