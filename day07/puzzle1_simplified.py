# -----------------------------------------------------------------------------
# Day 7, Part 1
#
# Each line represents a single equation. The test value appears before the colon on each line; it is
# your job to determine whether the remaining numbers can be combined with operators to produce the test value.
#
# Operators are always evaluated left-to-right, not according to precedence rules. Furthermore, numbers
# in the equations cannot be rearranged. Glancing into the jungle, you can see elephants holding two
# different types of operators: add (+) and multiply (*).
#
# Determine which equations could possibly be true. What is their total calibration result?
#
# -----------------------------------------------------------------------------

from typing import Iterator

# filename: str = 'sample.txt'
filename: str = 'input.txt'

# parse the input into a list of tuples, where each tuple then has two parts:
#  - the "test value" for the given equation
#  - a list of numbers in the equation
# go ahead and convert everything to integers now, since we need to do math on everything
equations: list[tuple] = []
for line in open(filename):
    test_val, nums = line.strip().split(': ')
    equations.append((int(test_val), [int(n) for n in nums.split(' ')]))


# 2 potential operators for each position means that there are 2^n possible combinations,
# where n is the number of missing operators
#
# first thing to know from this:
#  - in my input, the maximum number of missing operators is 12
#  - therefore, the maximum number of combinations is 2^12 = 4096
#  - that's a lot of lists to load into memory at one time, if we try to generate them all at once
#  - this function is written as a "generator" so it returns ("yields") each combination, one at a time,
#    and then comes back to where it was to get the next one, using an iterator
#
# second thing to recognize from this:
#  - Python already knows how to generate combinations of an arbitrary length,
#    where each position can be one of two choices - that's just a binary number string
#  - so, if we generate a binary number string of every number up to 2^n,
#    and if we zero-pad the number string, then we have generated all of the combinations,
#    so the last step is to convert that string to a list
def generate_operator_combinations(combo_count) -> Iterator[list[str]]:
    # use zero-padded binary number strings to build all of the combinations of operations needed for n positions
    for i in range(2**combo_count):
        yield list(format(i, f'0{combo_count}b'))


# given a combination of operators, execute the equation and compare the result to the test value
def validate_operators_for_equation(operators: list[str], operands: list[int], expected_result: int) -> bool:
    # because we follow operators in left to right order (and don't follow order of operations).
    # we can simply accumulate the result
    accumulator: int = operands[0]
    for i in range(len(operators)):
        # if our experimental value is already larger than the test value, we can abort - no need to keep calculating
        if accumulator > expected_result:
            return False
        # arbitrarily treat '0' as + and '1' as *
        if operators[i] == '0':
            accumulator += operands[i+1]
        else:
            accumulator *= operands[i+1]

    # did it work???
    return accumulator == expected_result


calibration: int = 0

# using the utility functions above makes this algorithm much easier to read

# for every equation we were given...
for test_value, numbers in equations:
    # for every possible combination of operators...
    for ops in generate_operator_combinations(len(numbers) - 1):
        # check to see if this set of operators would generate the test value
        if validate_operators_for_equation(ops, numbers, test_value):
            # if it worked, store it off
            calibration += test_value
            # there is no need to check any more operator combinations, because we found a working one for this equation
            break

# display the result
print(calibration)
