import re

# filename = 'sample.txt'
filename = 'input.txt'

parser = re.compile(r'(\d+)\s+(\d+)')
first = []
second = []
with open(filename) as file:
    for line in file:
        one, two = [int(i) for i in parser.match(line).groups()]
        first.append(one)
        second.append(two)

score = 0

while first:
    number = first.pop()
    score += number * second.count(number)

print(score)
