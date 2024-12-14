import math
import re
import time
from dataclasses import dataclass


@dataclass
class Robot:
    position: tuple[int, int]
    velocity: tuple[int, int]


# filename: str = 'sample.txt'; width: int = 11; height: int = 7
filename: str = 'input.txt'; width: int = 101; height: int = 103

parser = re.compile(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)')
robots_data = [parser.match(line).groups() for line in open(filename)]
robots = [Robot((int(data[0]), int(data[1])), (int(data[2]), int(data[3]))) for data in robots_data]

count = 0
found_count = 0
mid_x = width // 2
while True:
    count += 1
    grid = [['.' for x in range(width)] for y in range(height)]
    for robot in robots:
        x = (robot.position[0] + robot.velocity[0]) % width
        y = (robot.position[1] + robot.velocity[1]) % height
        robot.position = (x, y)
        grid[y][x] = '*'

    for row in grid:
        if row.count('*') > 30:
            for r in grid:
                print(''.join(r))
            print(count)
            found_count += 1
            if found_count > 10:
                exit()
            else:
                break
