# from pprint import pprint
from functools import cache

# filename: str = 'sample.txt'
filename: str = 'input.txt'

towel_line, design_lines = open(filename).read().split('\n\n')
towels: list[str] = towel_line.rstrip().split(', ')
designs: list[str] = design_lines.rstrip().split('\n')


@cache
def is_design_possible(design: str) -> bool:
    if len(design) == 0:
        # print('Success!')
        return True

    # print(design)
    for towel in towels:
        if design.startswith(towel):
            design_remaining = design.replace(towel, '', 1)
            # print(f'Found {towel}, trying {design_remaining}')
            if is_design_possible(design_remaining):
                return True

    # print('Failure.')
    return False


total_count = 0
good_count = 0
bad_count = 0

for d in designs:
    total_count += 1
    print(f'Combo {total_count}: ', end='', flush=True)
    if is_design_possible(d):
        good_count += 1
        print('good!')
    else:
        bad_count += 1
        print('not good.')

# I think the right answer is between 295 and 343 (was too high)
print(good_count)
print(bad_count)
