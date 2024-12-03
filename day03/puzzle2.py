import re

# filename = "sample2.txt"
filename = "input.txt"

parser: re.Pattern = re.compile(r'(don\'t)|(do)|mul\((\d+),(\d+)\)')
operators_and_pairs_of_numbers: list[tuple[str]] = parser.findall(open(filename).read())
product_sum = 0
enabled = True
while operators_and_pairs_of_numbers:
    match = operators_and_pairs_of_numbers.pop(0)
    if match[0] == "don't":
        enabled = False
    elif match[1] == "do":
        enabled = True
    else:
        if enabled:
            product_sum += int(match[2]) * int(match[3])
print(product_sum)
