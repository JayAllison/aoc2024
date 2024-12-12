from itertools import product

# filename: str = 'sample.txt'
filename: str = 'input.txt'

garden_map: list[str] = [line.rstrip() for line in open(filename).readlines()]
Y_MAX: int = len(garden_map)
X_MAX: int = len(garden_map[0])

unsorted_points: list[tuple] = [p for p in product(range(X_MAX), range(Y_MAX))]
up = (0, -1)
down = (0, +1)
left = (-1, 0)
right = (+1, 0)
directions: list = [left, right, up, down]
regions: list = []

while unsorted_points:
    starting_point: tuple = unsorted_points[0]
    check_points: set[tuple] = {starting_point}
    check_plant: str = garden_map[starting_point[1]][starting_point[0]]
    region_points: set = set()

    while check_points:
        check_this: tuple = check_points.pop()
        region_points.add(check_this)
        unsorted_points.remove(check_this)

        for dx, dy in directions:
            nx = check_this[0] + dx
            ny = check_this[1] + dy

            if (0 <= nx < X_MAX and 0 <= ny < Y_MAX
                    and garden_map[ny][nx] == check_plant
                    and (nx, ny) not in region_points):
                check_points.add((nx, ny))

    regions.append(region_points)

total_price = 0

for region in regions:
    corners = 0
    for plot in region:
        # check for outer corners - a single point can have more than one outer corner
        # check left and up for outside region
        # check up and right for outside region
        # check right and down for outside region
        # check down and left for outside region
        corner_checks = [(left, up), (up, right), (right, down), (down, left)]
        for c1, c2 in corner_checks:
            p1x = plot[0] + c1[0]
            p1y = plot[1] + c1[1]

            p2x = plot[0] + c2[0]
            p2y = plot[1] + c2[1]

            if (p1x, p1y) not in region and (p2x, p2y) not in region:
                corners += 1

            # check for inner corners - a single point can have more than one inner corner
            # check left and up for inside region, and diagonal for outside region
            # check up and right for inside region, and diagonal for outside region
            # check right and down for inside region, and diagonal for outside region
            # check down and left for outside region, and diagonal for outside region
            dx = plot[0] + c1[0] + c2[0]
            dy = plot[1] + c1[1] + c2[1]

            if (p1x, p1y) in region and (p2x, p2y) in region and (dx, dy) not in region:
                corners += 1

    total_price += len(region) * corners

print(total_price)
