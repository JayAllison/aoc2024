from collections import defaultdict

# filename = "sample.txt"
filename = "input.txt"

rules_section, updates_section = open(filename).read().split('\n\n')

rules_lines = rules_section.split('\n')
rules = defaultdict(list)
for rule in rules_lines:
    first, second = rule.split('|')
    rules[first].append(second)

updates = [pages.split(',') for pages in updates_section.split('\n') if pages]


def check_update(pages_to_update) -> bool:
    for i in range(len(pages_to_update)):
        for p in pages_to_update[0:i]:
            if p in rules[pages_to_update[i]]:
                return False
    return True


good_updates = []

for update in updates:
    if check_update(update):
        good_updates.append(update)

total = 0
for good in good_updates:
    total += int(good[len(good) // 2])

print(total)
