# -----------------------------------------------------------------------------
# Day 8, Part 1
#
# the puzzle:
#
# An antinode occurs at any point that is perfectly in line with two antennas of the same frequency,
# but only when one of the antennas is twice as far away as the other. This means that for any pair
# of antennas with the same frequency, there are two antinodes, one on either side of them.
#
# How many unique locations within the bounds of the map contain an antinode?
#
# explanation of this solution:
#
# this solution is greatly simplified by using Python's built-in iterator utility functions,
# so I am going to leave them in the puzzle (rather than replace them with code of my own)
# and explain what they are doing and how they are used
#
# if you have been following along since Day 1, you should have already seen some of these same
# concepts explained more thoroughly, so there is no need to do that again here.
#
# -----------------------------------------------------------------------------

from collections import defaultdict
from itertools import combinations, product

# filename: str = 'sample.txt'
filename: str = 'input.txt'

# parse the map into a list of strings that we will treat like a 2D array
# we can leave the rows as strings (instead of lists) because we don't need to edit them,
# but if you split the row string into a list, the code would work exactly the same way
# remember that the outer index is Y and the inner index is X, which is backwards from math class
# so the point (x, y) is antenna_map[y][x]
antenna_map: list[str] = [line.rstrip() for line in open(filename).readlines()]

# calculate the boundaries for this map - as with all of the 2D maps in AoC so far this year, this one is also square
# remember that the Pythonic convention is to put constant value in all caps
Y_MAX: int = len(antenna_map)
X_MAX:int  = len(antenna_map[0])

# using defaultdict instead of the plain dict just makes it easier to add each key to the dict the first time
# otherwise, we would need to check for whether the key was already in the list,
# and if it wasn't, we'd need to create the list and add the value,
# and if it was, we'd need to only add the value
# using defaultdict just makes that cleaner - it will create the list behind the scenes when needed,
# so all we need to do is just append to the list - we don't need to check first to see if it exists
antenna_locations: dict[str: list] = defaultdict(list)

# parse the input into lists of antenna positions by name/frequency
# itertools.product() makes a Cartesian product, so this one line makes a list of all of the (x,y) points on the map
# we could otherwise use two nested for loops (like we did on previous days) and still have the same overall result
for x, y in product(range(X_MAX), range(Y_MAX)):
    # if we found an antenna, store its location based the frequency of the antenna
    if antenna_map[y][x] != '.':
        antenna_locations[antenna_map[y][x]].append((x, y))

# we were asked for unique locations - using a set() eliminates duplicates for us without any extra effort
antinode_locations: set[tuple] = set()

# execute the algorithm: find the antinodes for each frequency
for frequency in antenna_locations:
    # the puzzle asks us to compare, for each given frequency, each unique pair of antennas
    # we already have a list of all of the antenna locations for a given frequency
    # the itertools.combinations() utility can pair those up for us, without any extra work on our part
    # otherwise, we'd have to write out own n choose 2 algorithm (likely using nested loops)
    for first_antenna_pos, second_antenna_pos in combinations(antenna_locations[frequency], 2):

        # calculate the x,y distance between the two points in this combination of antenna locations,
        # and then use that distance to find the antinodes
        # as long as we are consistent about which one is first and which one is second,
        # then the math works out right, even if the second is "before" the first
        delta_x: int = second_antenna_pos[0] - first_antenna_pos[0]
        delta_y: int = second_antenna_pos[1] - first_antenna_pos[1]

        # the first antinode is the first point minus the calculated distance
        antinode1_x: int = first_antenna_pos[0] - delta_x
        antinode1_y: int = first_antenna_pos[1] - delta_y

        # the second antinode is the second point plus the calculated distance
        antinode2_x: int = second_antenna_pos[0] + delta_x
        antinode2_y: int = second_antenna_pos[1] + delta_y

        # only keep antinodes that appear within the boundaries of the map
        # using this simply loop, we don't have to copy & paste code (which creates the potential for errors)
        for nx, ny in [(antinode1_x, antinode1_y), (antinode2_x, antinode2_y)]:
            if 0 <= nx < X_MAX and 0 <= ny < Y_MAX:
                antinode_locations.add((nx, ny))

# display the result
print(len(antinode_locations))
