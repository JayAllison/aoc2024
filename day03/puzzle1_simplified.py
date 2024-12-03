import re

# -----------------------------------------------------------------------------
# First part of Day 3:
#
# The computer appears to be trying to run a program. It seems like the goal of the
# program is just to multiply some numbers. It does that with instructions like mul(X,Y),
# where X and Y are each 1-3 digit numbers.
#
# However, because the program's memory has been corrupted, there are also many invalid
# characters that should be ignored, even if they look like part of a mul instruction.
#
# Scan the corrupted memory for uncorrupted mul instructions. What do you get if you add
# up all of the results of the multiplications?
#
# -----------------------------------------------------------------------------

# using regex, the solution for this puzzle is short & sweet

# filename = "sample.txt"
filename = "input.txt"

# there is no need to worry about keeping lines separate - pull everything into a single string
line: str = open(filename).read()

# Some useful regex resources:
#   - Learn:      https://regexlearn.com/learn/regex101
#   - Experiment: https://regex101.com/

# this regular expression finds mul(xxx,yyy) and extracts x & y into separate groups
# the puzzle is explicit about the formatting, which simplifies the regex
parser: re.Pattern = re.compile(r'mul\((\d+),(\d+)\)')

# findall() will find every match of the regex within the string and
# will return a list of everything that has been found
# each match's groups are returned as a separate tuple in that list
# also, there's no reason we must convert the number strings to integers here
pairs_of_numbers: list[tuple[str]] = parser.findall(line)

product_sum: int = 0

while pairs_of_numbers:
    # for part 1, it does not matter whether we go forward or backward
    # since pop() is more efficient than pop(0), we'll choose efficiency
    pair: tuple[str] = pairs_of_numbers.pop()

    # execute the puzzle operation: sum the products
    # I found it easiest to convert the number strings to integers at this step
    product_sum += int(pair[0]) * int(pair[1])

# display the result
print(product_sum)
