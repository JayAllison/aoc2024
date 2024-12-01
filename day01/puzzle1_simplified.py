# -----------------------------------------------------------------------------
# First part of Day 1:
#
# Pair up the numbers and measure how far apart they are.
# Pair up the smallest number in the left list with the smallest number in the right list,
# then the second-smallest left number with the second-smallest right number, and so on.
#
# Within each pair, figure out how far apart the two numbers are;
# you'll need to add up all of those distances.
# -----------------------------------------------------------------------------

# filename: str = 'sample.txt'
filename: str = 'input.txt'

left: list[int] = []
right: list[int] = []

# read in each line from the file, then split out the first and second numbers
# convert those number strings to integers and store in separate lists
with open(filename) as file:
    for line in file:
        numbers: list[str] = line.split('   ')
        left.append(int(numbers[0]))
        right.append(int(numbers[1]))

# Python allows lists (and only lists) to be sorted in place:
#   "list.sort() modifies the list in-place... if you don’t need the original list, it’s slightly more efficient."
#   https://docs.python.org/3/howto/sorting.html
left.sort()
right.sort()

# find the difference between each pair and add that difference to the total
total: int = 0
for i in range(len(left)):
    difference = left[i] - right[i]
    total += abs(difference)

# display the result
print(total)
