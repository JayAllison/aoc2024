from collections import defaultdict, deque

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


def fix_update(pages_to_update) -> list:
    corrected = []
    for i in range(len(pages_to_update)):
        newly_corrected = []
        corrections = []
        for j in range(len(corrected)):
            if corrected[j] in rules[pages_to_update[i]]:
                corrections.append(corrected[j])
            else:
                newly_corrected.append(corrected[j])
        newly_corrected.append(pages_to_update[i])
        newly_corrected.extend(corrections)
        corrected = newly_corrected

    return corrected


corrected_updates = []

for update in updates:
    if not check_update(update):
        corrected_updates.append(fix_update(update))


total = 0
for good in corrected_updates:
    total += int(good[len(good) // 2])

print(total)
