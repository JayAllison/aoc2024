# -----------------------------------------------------------------------------
# Day 11, Part 1
#
# Stones are arranged in a perfectly straight line, and each stone has a number engraved on it.
# Every time you blink, the stones change. Sometimes, the number engraved on a stone changes.
# Other times, a stone might split in two, causing all the other stones to shift over a bit
# to make room in their perfectly straight line.
#
# Every time you blink, the stones each simultaneously change according to the first applicable rule in this list:
#
#  - If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
#  - If the stone is engraved with a number that has an even number of digits, it is replaced by two stones.
#    The left half of the digits are engraved on the new left stone, and the right half of the digits are
#    engraved on the new right stone. (The new numbers don't keep extra leading zeroes.)
#  - If none of the other rules apply, the stone is replaced by a new stone; the old stone's number
#    multiplied by 2024 is engraved on the new stone.
#
# No matter how the stones change, their order is preserved, and they stay on their perfectly straight line.
#
# -----------------------------------------------------------------------------

# filename: str = 'sample.txt'
filename: str = 'input.txt'

# a list holding the starting set of stones - read in the single line of input, split into integers
stones: list[int] = [int(_stone) for _stone in open(filename).readline().rstrip().split(' ')]

# How many stones will you have after blinking 25 times?
REPEATS: int = 25

# `repeat` is 1-n, indicating which round we're on - I want 0 to indicate the initial round, which is why
# this range() looks different than normal - that does not really matter unless you're debugging, though
for repeat in range(1, REPEATS + 1, 1):
    # a new list to hold the new set of stones, after each blink
    new_stones: list[int] = []

    # iterate over each stone in the staring list, and apply the algorithm to generate the replacement stone(s)
    for stone in stones:
        # If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1
        if stone == 0:
            new_stones.append(1)
        # If the stone is engraved with a number that has an even number of digits, it is replaced by two stones
        elif len(str(stone)) % 2 == 0:
            # convert the integer to a string to make splitting in half easier
            number = str(stone)
            # the left half of the digits are engraved on the new left stone
            # use a slice to get the first half of the string, then convert back to an integer
            first = int(number[0:len(number)//2])
            new_stones.append(first)
            # the right half of the digits are engraved on the new right stone
            # use a slice to get the second half of the string, then convert back to an integer
            second = int(number[len(number)//2:])
            new_stones.append(second)
        # the old stone's number multiplied by 2024 is engraved on the new stone.
        else:
            new_stones.append(2024 * stone)

    # the new list becomes the starting list for the next round
    stones = new_stones

# display the result - how many stones did we end up with?
print(len(stones))
