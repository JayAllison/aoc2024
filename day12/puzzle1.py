# -----------------------------------------------------------------------------
# Day 12, Part 1
#
# They hand you a map (your puzzle input) of the garden plots. Each garden plot grows only a single type
# of plant and is indicated by a single letter on your map. When multiple garden plots are growing the
# same type of plant and are touching (horizontally or vertically), they form a region.
#
# In order to accurately calculate the cost of the fence around a single region, you need to know that
# region's area and perimeter.
#
# The area of a region is simply the number of garden plots the region contains. The perimeter of a region
# is the number of sides of garden plots in the region that do not touch another garden plot in the same region.
#
# -----------------------------------------------------------------------------

from itertools import product

# filename: str = 'sample.txt'
filename: str = 'input.txt'

# parse the map into a list of strings that we will treat like a 2D array (like many other days)
# we can leave the rows as strings (instead of lists) because we don't need to edit them,
# but if you split the row string into a list, the code would work exactly the same way
# remember that the outer index is Y and the inner index is X, which is backwards from math class
# so the point/plot (x, y) is garden_map[y][x]
garden_map: list[str] = [line.rstrip() for line in open(filename).readlines()]

# same as the other days - this pattern should be clear by now:
# calculate the boundaries for this map - as with all of the 2D maps in AoC so far this year, this one is also square
# remember that the Pythonic convention is to put constant value in all caps
Y_MAX: int = len(garden_map)
X_MAX: int = len(garden_map[0])

# to search for separate regions, we start with a list of ALL of the points on the map - these are the unsorted "plots"
# every time we identify that a point is within a region, we will remove it from this list
# this makes sure we don't miss any points, since we are not searching linearly
unsorted_points: list[tuple] = [p for p in product(range(X_MAX), range(Y_MAX))]

# what directions can we search in? making a list like this lets us use a loop below instead of duplicating code
# implied by puzzle: regions don't extend diagonally - only up, down, left, or right (from the perspective of the map)
directions: list = [(-1, 0), (+1, 0), (0, -1), (0, +1)]

# a list of sets, each set is all of the points/plots within a region
regions: list = []

# once this is empty, we have sorted every point/plot into a region
while unsorted_points:

    # start the search for the next region with a point from the unsorted list - we'll start with 0, but it could be any
    # don't add this to the region list yet - wait until we have checked all around it for like plants
    starting_point: tuple = unsorted_points[0]

    # this set of points is the points we need to search around for like plants
    # once this list is empty, the full region has been identified
    # using a set helps prevent us from checking a point twice
    check_points: set[tuple] = {starting_point}

    # the type of plant in this region, based on the starting point
    check_plant: str = garden_map[starting_point[1]][starting_point[0]]

    # all of the unique points/plots in this region - using a set prevents us from counting a point twice
    region_points: set = set()

    # search adjacent points until we have exhausted this checklist
    while check_points:

        # we can remove this point from the checklist now that we are checking it
        check_this: tuple = check_points.pop()

        # we know this is a region point - add it to the list and remove it from the unsorted list
        region_points.add(check_this)
        unsorted_points.remove(check_this)

        # check adjacent points - if they are valid map points, and they are the same plant,
        # and we have not already found them, add them to the set of points to check
        for dx, dy in directions:
            nx = check_this[0] + dx
            ny = check_this[1] + dy

            if (0 <= nx < X_MAX and 0 <= ny < Y_MAX
                    and garden_map[ny][nx] == check_plant
                    and (nx, ny) not in region_points):
                check_points.add((nx, ny))

    # add this new region to the list of regions we've identified
    regions.append(region_points)

# per the puzzle, the cost of each region is the area * the perimeter
total_price = 0

# calculate the price of each region individually
for region in regions:
    # calculate the perimeter of the region by counting edges that face out
    perimeter = 0
    for plot in region:
        for dx, dy in directions:
            nx = plot[0] + dx
            ny = plot[1] + dy

            if (nx, ny) not in region:
                perimeter += 1

    # the area is simply the number of points/plots in the region
    # so, using the perimeter that we just calculated, add this region's price to the total
    total_price += len(region) * perimeter

# display the result
print(total_price)
