import itertools

# filename = "sample.txt"
filename = "input.txt"

board = [line.rstrip() for line in open(filename).readlines()]
y_max = len(board)
x_max = len(board[0])

starts = [(x, y) for x, y in itertools.product(range(x_max), range(y_max)) if board[y][x] == 'X']

directions = [(x, y) for x in (-1, 0, +1) for y in (-1, 0, +1) if x != 0 or y != 0]

count = 0
for x_s, y_s in starts:
    for dx, dy in directions:
        x, y = (x_s + dx, y_s + dy)
        if 0 <= x < x_max and 0 <= y < y_max and board[y][x] == 'M':
            x, y = (x + dx, y + dy)
            if 0 <= x < x_max and 0 <= y < y_max and board[y][x] == 'A':
                x, y = (x + dx, y + dy)
                if 0 <= x < x_max and 0 <= y < y_max and board[y][x] == 'S':
                    count += 1

print(count)
