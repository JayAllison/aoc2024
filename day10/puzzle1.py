import itertools

# filename: str = 'sample.txt'
filename: str = 'input.txt'

topo_map: list[list[int]] = [[int(p) for p in line.rstrip()] for line in open(filename).readlines()]
Y_MAX: int = len(topo_map)
X_MAX: int = len(topo_map[0])

trailheads = []

for thx, thy in itertools.product(range(X_MAX), range(Y_MAX)):
    if topo_map[thy][thx] == 0:
        trailheads.append((thx, thy))

directions = [(-1, 0), (+1, 0), (0, -1), (0, +1)]
total = 0

for x, y in trailheads:
    score = 0
    peaks_found = []
    next_steps = [(x, y)]
    for sx, sy in next_steps:
        for direction in directions:
            nx, ny = sx + direction[0], sy + direction[1]
            if 0 <= nx < X_MAX and 0 <= ny < Y_MAX and topo_map[ny][nx] == topo_map[sy][sx] + 1:
                if topo_map[ny][nx] == 9 and (nx, ny) not in peaks_found:
                    score += 1
                    peaks_found.append((nx, ny))
                else:
                    next_steps.append((nx, ny))
    total += score

print(total)
