from pprint import pprint

# filename: str = 'sample.txt'
filename: str = 'input.txt'

equations = []
for line in open(filename):
    test_val, nums = line.strip().split(': ')
    equations.append((int(test_val), [int(n) for n in nums.split(' ')]))


def generate_operator_combinations(combo_count) -> list[list[str]]:
    # use zero-padded binary number strings to build all of the combinations of operations needed for n positions
    for i in range(2**combo_count):
        yield list(format(i, f'0{combo_count}b'))


def validate_operators_for_equation(operators: list[str], operands: list[int], expected_result: int) -> bool:
    accumulator = operands[0]
    for i in range(len(operators)):
        if accumulator > expected_result:
            return False
        # arbitrarily treat '0' as + and '1' as *
        if operators[i] == '0':
            accumulator += operands[i+1]
        else:
            accumulator *= operands[i+1]

    return accumulator == expected_result


calibration = 0
for test_value, numbers in equations:
    for ops in generate_operator_combinations(len(numbers) - 1):
        if validate_operators_for_equation(ops, numbers, test_value):
            calibration += test_value
            break

print(calibration)
