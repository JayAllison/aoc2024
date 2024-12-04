# filename = "sample.txt"
filename = "input.txt"

lines = [line.rstrip() for line in open(filename).readlines()]

starts = []
y_max = len(lines)
x_max = len(lines[0])


def check_mas(a: tuple, m: list[tuple], s: list[tuple]) -> bool:
    x_m1 = a[0] + m[0][0]
    y_m1 = a[1] + m[0][1]
    x_m2 = a[0] + m[1][0]
    y_m2 = a[1] + m[1][1]

    x_s1 = a[0] + s[0][0]
    y_s1 = a[1] + s[0][1]
    x_s2 = a[0] + s[1][0]
    y_s2 = a[1] + s[1][1]

    if 0 <= x_m1 < x_max and 0 <= y_m1 < y_max and lines[y_m1][x_m1] == 'M':
        if 0 <= x_m2 < x_max and 0 <= y_m2 < y_max and lines[y_m2][x_m2] == 'M':
            if 0 <= x_s1 < x_max and 0 <= y_s1 < y_max and lines[y_s1][x_s1] == 'S':
                if 0 <= x_s2 < x_max and 0 <= y_s2 < y_max and lines[y_s2][x_s2] == 'S':
                    return True

    return False


for yy in range(y_max):
    for xx in range(x_max):
        if lines[yy][xx] == 'A':
            starts.append((xx, yy))

up = [(-1, -1), (+1, -1)]
dn = [(-1, +1), (+1, +1)]
lt = [(-1, -1), (-1, +1)]
rt = [(+1, -1), (+1, +1)]

count = 0
for point in starts:
    if check_mas(point, up, dn) or check_mas(point, dn, up) or check_mas(point, lt, rt) or check_mas(point, rt, lt):
        count += 1

print(count)
