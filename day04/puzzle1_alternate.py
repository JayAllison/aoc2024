import itertools

# filename = "sample.txt"
filename = "input.txt"

board = [line.rstrip() for line in open(filename).readlines()]
y_max = len(board)
x_max = len(board[0])

directions = [(dx, dy) for dx in (-1, 0, +1) for dy in (-1, 0, +1) if dx != 0 or dy != 0]


def check_for_word_in_direction(word, point, direction) -> bool:
    for i in range(1,len(word)):
        x, y = (point[0] + direction[0]*i, point[1] + direction[1]*i)
        if x < 0 or x >= x_max or y < 0 or y >= y_max or board[y][x] != word[i]:
            return False

    return True


def check_for_word_at(word, point) -> int:
    if board[point[1]][point[0]] != word[0]:
        return 0

    return [check_for_word_in_direction(word, point, d) for d in directions].count(True)


search_word = 'XMAS'
words_found = [check_for_word_at(search_word, (px, py)) for px, py in itertools.product(range(x_max), range(y_max))]
print(sum(words_found))
