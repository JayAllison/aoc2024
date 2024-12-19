# from pprint import pprint
from functools import cache

# filename: str = 'sample.txt'
filename: str = 'input.txt'

towel_line, design_lines = open(filename).read().split('\n\n')
towels: list[str] = towel_line.rstrip().split(', ')
designs: list[str] = design_lines.rstrip().split('\n')


@cache
def is_design_possible(design: str) -> int:
    found = 0

    if len(design) == 0:
        # print('Success!')
        return 1

    # print(design)
    for towel in towels:
        if design.startswith(towel):
            design_remaining = design.replace(towel, '', 1)
            # print(f'Found {towel}, trying {design_remaining}')
            if nested_found := is_design_possible(design_remaining):
                found += nested_found

    # print('Failure.')
    return found


total_count: int = 0
counter: int = 0

for d in designs:
    counter += 1
    # print(f'Combo {counter}: ', end='', flush=True)
    if count := is_design_possible(d):
        total_count += count
        # print(f'{count} good!')
    else:
        # print('not good.')
        pass

print(total_count)
