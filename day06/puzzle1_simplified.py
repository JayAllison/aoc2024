# -----------------------------------------------------------------------------
# Day 5, Part 1:
#
# The map shows the current position of the guard with ^ (to indicate the guard is currently facing up
# from the perspective of the map). Any obstructions are shown as #.
#
# Lab guards follow a very strict patrol protocol which involves repeatedly following these steps:
#
#   - If there is something directly in front of you, turn right 90 degrees.
#   - Otherwise, take a step forward.
#
# Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?
# -----------------------------------------------------------------------------

# filename: str = "sample.txt"
filename: str = "input.txt"

# same as Day 4, read the file into a 2D array, where:
#   outer index is Y (line), inner index is X (column), (0,0) is upper left, (y, x) is lower right
# we could split the row into a list of characters, but since we don't need to edit (at least, in Part 1),
# then that's not necessary - we can index into strings just as easily
# if board[y][x] bothers you, you could "transpose" the matrix - check online for ways of doing so
lab_map: list[str] = []
for line in open(filename):
    lab_map.append(line.rstrip())

# same as Day 4, we will use these bounds several times, so go ahead and store them with useful names
# Python does not support true constant value, but convention says that constant variables should be all uppercase
# this assumes that every row is the same length (and it is)
# actually, for this puzzle, like Day 4, the board is square - we could even choose to combine, if we wanted to
Y_MAX: int = len(lab_map)
X_MAX: int = len(lab_map[0])


# a utility function to test the point we're about to look at against the bounds of the map
def is_within_map(point: tuple) -> bool:
    return 0 <= point[0] < X_MAX and 0 <= point[1] < Y_MAX


# if we turn right 90 degrees every time we hit an obstacle, then this is the progression of directions we will face
# using strings is not strictly necessary, but I think it makes it easier to view the algorithm in human-readable form
# why use North, East, South, West instead of Up, Right, Down, Left? no reason - just pick one.
directions: list[str] = ['N', 'E', 'S', 'W']

# this is the (x,y) move we need to make next, based on the direction that we are currently facing
# remember that on our map, (0,0) is the upper left, so the Y axis is reversed from how you think of it in math class
moves: dict[str: tuple] = {
    'N': (+0, -1),  # moving  North (up)     means moving -1 in the Y direction
    'E': (+1, +0),  # moving  East  (right)  means moving +1 in the X direction
    'S': (+0, +1),  # moving  South (down)   means moving +1 in the Y direction
    'W': (-1, +0)   # moving  West  (left)   means moving -1 in the X direction
}

# keep track of which spots on the map we have visited - start with an empty container
# using a set means we won't count a position more than once, no matter how many times we pass through it
visited: set = set()

# by puzzle definition, we start out facing North
current_dir: int = directions.index('N')

# an initial value, to make my IDE happy - we know for sure we will find the ^ in the map, but my IDE does not know that
current_pos: tuple = (-1, -1)

# check every point on the map until we find the starting point, then save it off and stop the search
for x in range(X_MAX):
    for y in range(Y_MAX):
        if lab_map[y][x] == '^':
            current_pos = (x, y)
            break

# the puzzle tells us to keep walking until we leave the map area - that means we need a while loop, not a for loop
while is_within_map(current_pos):

    # record that we have visited this position - again, using set keeps us from counting this position twice
    visited.add(current_pos)

    # using the current direction we are facing, calculate the next position to move to, based on the current position
    move_by_x, move_by_y = moves[directions[current_dir]]
    current_x, current_y = current_pos
    next_x, next_y = (current_x + move_by_x, current_y + move_by_y)

    # check for an obstacle: move forward or turn?
    # but, we can't check for an obstacle unless we first check to see if we just walked off the map
    if is_within_map((next_x, next_y)) and lab_map[next_y][next_x] == '#':
        # if we find an obstacle, turn 90 degrees
        # advance to the next direction in the direction list, wrapping back to the beginning when needed
        current_dir = (current_dir + 1) % len(directions)
    else:
        # if we did not find an obstacle, step forward
        # if we just stepped off the map, the loop will end and we'll be done
        current_pos = (next_x, next_y)

# display the result
print(len(visited))
