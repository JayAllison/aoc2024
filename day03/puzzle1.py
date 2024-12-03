from functools import reduce
import re

# filename = "sample.txt"
filename = "input.txt"

parser: re.Pattern = re.compile(r'mul\((\d+),(\d+)\)')
pairs_of_numbers: list[tuple[str]] = parser.findall(open(filename).read())
print(reduce(lambda a, t: a + int(t[0]) * int(t[1]), pairs_of_numbers, 0))
