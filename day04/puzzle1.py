import itertools

# filename = "sample.txt"
filename = "input.txt"

lines = [line.rstrip() for line in open(filename).readlines()]

starts = []
y_max = len(lines)
x_max = len(lines[0])

for y in range(y_max):
    for x in range(x_max):
        if lines[y][x] == 'X':
            starts.append((x, y))

directions = list(itertools.product([-1, 0, 1], [-1, 0, 1]))
directions.remove((0, 0))

count = 0
for x_s, y_s in starts:
    for dx, dy in directions:
        x = x_s + dx
        y = y_s + dy
        if 0 <= x < x_max and 0 <= y < y_max and lines[y][x] == 'M':
            x += dx
            y += dy
            if 0 <= x < x_max and 0 <= y < y_max and lines[y][x] == 'A':
                x += dx
                y += dy
                if 0 <= x < x_max and 0 <= y < y_max and lines[y][x] == 'S':
                    count += 1

print(count)
