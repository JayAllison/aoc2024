import itertools

# filename = "sample.txt"
filename = "input.txt"

# read the file into a 2D array, where:
#   outer index is Y (line), inner index is X (column), (0,0) is upper left, (y, x) is lower right
# we could split the row into a list of characters, but since we don't need to edit,
# that's not necessary - we can index into strings just as easily
# if board[y][x] bothers you, you could "transpose" the matrix - check online for ways of doing so
board: list[str] = []
for line in open(filename).readlines():
    board.append(line.rstrip())

# we will use these bounds several times, so go ahead and store them with useful names
# this assumes that every row is the same length (and it is)
# actually, for this puzzle, the board is square - we could even choose to combine, if we wanted to
y_max = len(board)
x_max = len(board[0])

# we need to "read" the word from the center X in each of these directions:
#    \ | /
#    - X -
#    / | \
# because this is symmetric, it does not matter which one is X and which one is Y
moves: list[tuple] = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

# check every position on the board and record points where the board position is 'X'
starting_points: list[tuple] = []
for x in range(x_max):
    for y in range(y_max):
        if board[y][x] == 'X':
            starting_points.append((x, y))

count = 0

# from every starting point that we found, check letter by letter in each direction for the word we're looking for
# be sure not to go out of bounds (off the edge of the board)
# we could have put this under the foor loop above and eliminated the need for the starting_points variable,
# but that nesting would be *very* deep
# though exercise: how could you change this to work for any word instead of one specific, hardcoded word?
for x_s, y_s in starting_points:
    for dx, dy in moves:
        x, y = (x_s + dx, y_s + dy)
        if 0 <= x < x_max and 0 <= y < y_max and board[y][x] == 'M':
            x, y = (x + dx, y + dy)
            if 0 <= x < x_max and 0 <= y < y_max and board[y][x] == 'A':
                x, y = (x + dx, y + dy)
                if 0 <= x < x_max and 0 <= y < y_max and board[y][x] == 'S':
                    count += 1

# display the output
print(count)
