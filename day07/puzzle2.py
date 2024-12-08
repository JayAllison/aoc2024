from datetime import datetime
from typing import Iterator

# filename: str = 'sample.txt'
filename: str = 'input.txt'

equations = []
for line in open(filename):
    test_val, nums = line.strip().split(': ')
    equations.append((int(test_val), [int(n) for n in nums.split(' ')]))


operator_characters = '+*|'


def generate_operator_combinations(combo_count, start=None) -> Iterator[list[str]]:
    if not start:
        start = []
    for operator in operator_characters:
        working = start.copy()
        working.append(operator)
        if len(working) < combo_count:
            yield from generate_operator_combinations(combo_count, working)
        else:
            yield working


def validate_operators_for_equation(operators: list[str], operands: list[int], expected_result: int) -> bool:
    accumulator = operands[0]
    for i in range(len(operators)):
        if accumulator > expected_result:
            return False
        if operators[i] == '+':
            accumulator += operands[i+1]
        elif operators[i] == '*':
            accumulator *= operands[i+1]
        elif operators[i] == '|':
            accumulator = int(str(accumulator) + str(operands[i+1]))

    return accumulator == expected_result


before = datetime.now()
print(f'Starting evaluation at {before}')

calibration = 0
for test_value, numbers in equations:
    for ops in generate_operator_combinations(len(numbers) - 1):
        if validate_operators_for_equation(ops, numbers, test_value):
            calibration += test_value
            break

print(f'Completed in {datetime.now() - before}')
print(calibration)
