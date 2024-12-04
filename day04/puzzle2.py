import itertools

# filename = "sample.txt"
filename = "input.txt"

board = [line.rstrip() for line in open(filename).readlines()]
y_max = len(board)
x_max = len(board[0])


def check_for_mas(a: tuple, m: list[tuple], s: list[tuple]) -> bool:
    x_m1, y_m1 = (a[0] + m[0][0], a[1] + m[0][1])
    x_m2, y_m2 = (a[0] + m[1][0], a[1] + m[1][1])

    x_s1, y_s1 = (a[0] + s[0][0], a[1] + s[0][1])
    x_s2, y_s2 = (a[0] + s[1][0], a[1] + s[1][1])

    if 0 <= x_m1 < x_max and 0 <= y_m1 < y_max and board[y_m1][x_m1] == 'M':
        if 0 <= x_m2 < x_max and 0 <= y_m2 < y_max and board[y_m2][x_m2] == 'M':
            if 0 <= x_s1 < x_max and 0 <= y_s1 < y_max and board[y_s1][x_s1] == 'S':
                if 0 <= x_s2 < x_max and 0 <= y_s2 < y_max and board[y_s2][x_s2] == 'S':
                    return True

    return False


starts = [(x, y) for x, y in itertools.product(range(x_max), range(y_max)) if board[y][x] == 'A']

up = [(-1, -1), (+1, -1)]
dn = [(-1, +1), (+1, +1)]
lt = [(-1, -1), (-1, +1)]
rt = [(+1, -1), (+1, +1)]

count = 0
for pt in starts:
    if check_for_mas(pt, up, dn) or check_for_mas(pt, dn, up) or check_for_mas(pt, lt, rt) or check_for_mas(pt, rt, lt):
        count += 1

print(count)
