# -----------------------------------------------------------------------------
# Second part of Day 1:
#
# You'll need to figure out exactly how often each number from the left list appears in
# the right list. Calculate a total similarity score by adding up each number in the left
# list after multiplying it by the number of times that number appears in the right list.
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

# multiply each number in the left list by the number of times it appears in the right list
# and add that to the total score
score: int = 0
for i in range(len(left)):
    count = right.count(left[i])
    score += left[i] * count

# display the result
print(score)
