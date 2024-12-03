import re

# filename = "sample.txt"
filename = "input.txt"

parser: re.Pattern = re.compile(r'mul\((\d+),(\d+)\)')
pairs_of_numbers: list[tuple[str]] = parser.findall(open(filename).read())
product_sum = 0
while pairs_of_numbers:
    pair = pairs_of_numbers.pop()
    product_sum += int(pair[0]) * int(pair[1])
print(product_sum)
