import re

# -----------------------------------------------------------------------------
# Second part of Day 3:
#
# There are two new instructions you'll need to handle:
#
#   - The do() instruction enables future mul instructions.
#   - The don't() instruction disables future mul instructions.
#
# Only the most recent do() or don't() instruction applies.
#
# At the beginning of the program, mul instructions are enabled.
#
# -----------------------------------------------------------------------------

# using regex, the solution for this puzzle is short & sweet

# filename = "sample2.txt"  # note that the example for Part 2 is different from Part 1
filename = "input.txt"

# there is no need to worry about keeping lines separate - pull everything into a single string
line: str = open(filename).read()

# Some useful regex resources:
#   - Learn:      https://regexlearn.com/learn/regex101
#   - Experiment: https://regex101.com/

# this regular expression is a little more robust - it is looking for one of three things:
#    1. the literal string "don't()"
#    2. the literal string "do()"
#    3. extracting x & y the phrase mul(xxx,yyy)
# The values found are extracted into groups
# Using the or operator ('|') lets us combine all of these searches into a single regex
parser: re.Pattern = re.compile(r'(do\(\))|(don\'t\(\))|mul\((\d+),(\d+)\)')

# findall() will find every match of the regex within the string and return a list of everything that has been found,
# in the order (left to right) that the matches were found - preserving this order does a lot of the work for us
# each match's groups are returned as a separate tuple in that list
# we have four groups, so there will be four elements in the tuple - the ones that are found will be populated, and
# the ones that aren't found will be empty strings ('')
# also, there's no reason we must convert the number strings to integers here
operators_and_pairs_of_numbers: list[tuple[str]] = parser.findall(line)

product_sum: int = 0
enabled = True

while operators_and_pairs_of_numbers:

    # for part 2, left-to-right order *does* matter, so we must pop(0)
    # performance seems adequate just using a list, but we could have converted to a deque if needed
    match = operators_and_pairs_of_numbers.pop(0)

    # check what we found - are we disabling, enabling, or multiplying?
    # fortunately the puzzle does not have anything else tricky about the sequencing of the operators
    if match[0] == "do()":
        enabled = True
    elif match[1] == "don't()":
        enabled = False
    else:
        # execute the puzzle operation: sum the products only when enabled
        if enabled:
            # I found it easiest to convert the number strings to integers at this step
            product_sum += int(match[2]) * int(match[3])

# display the output
print(product_sum)
