import math
import re
from dataclasses import dataclass

# classes in Python are an easy way to group like data and give it names,
# and dataclasses are a lightweight style of class that's quick & easy to use
@dataclass
class Robot:
    position: tuple[int, int]
    velocity: tuple[int, int]

# for today's puzzle, we have additional input values that are not in the input file
# by putting that all on the same line, it makes it easier to switch between test data and real data
# filename: str = 'sample.txt'; width: int = 11; height: int = 7
filename: str = 'input.txt'; width: int = 101; height: int = 103

# a regular expression to extract the four number strings from the specified
# accounting for the - sign that appears sometimes on two of the values
parser = re.compile(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)')

# first, extract the four number strings into a list for each robot
robots_data = [parser.match(line).groups() for line in open(filename)]

# next, convert to integers and store in a dataclass instance for each robot
robots = [Robot((int(data[0]), int(data[1])), (int(data[2]), int(data[3]))) for data in robots_data]

# Part 1 says to run the simulation for 100 seconds
time = 100
for second in range(time):
    for robot in robots:
        # the definition of the puzzle makes the movement calculations pretty easy
        # add the delta-x value to the current x position, add the delta-y value to the current y position,
        # and wrap if needed
        x = (robot.position[0] + robot.velocity[0]) % width
        y = (robot.position[1] + robot.velocity[1]) % height
        # update the robot with its new position
        robot.position = (x, y)

# Part 1 asks us to count the number of robots in each quadrant, then multiply those counts together
# it doesn't matter which quadrant is 1, 2, 3, 4
quadrant_count = [0, 0, 0, 0]
for robot in robots:
    x, y = robot.position

    # robots on the center line don't count, so use < and >
    if x < width // 2 and y < height // 2:
        quadrant_count[0] += 1
    elif x < width // 2 and y > height // 2:
        quadrant_count[1] += 1
    elif x > width // 2 and y < height // 2:
        quadrant_count[2] += 1
    elif x > width // 2 and y > height // 2:
        quadrant_count[3] += 1

# sum() is built into Python, but product() comes from a library
print(math.prod(quadrant_count))
