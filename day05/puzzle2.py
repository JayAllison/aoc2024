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


def correct_in_place(pages_to_correct) -> None:
    for i in range(len(pages_to_correct)):
        violations = rules[pages_to_correct[i]]
        j = 0
        end = i
        while j < end:
            if pages_to_correct[j] in violations:
                pages_to_correct.insert(i, pages_to_correct.pop(j))
                end -= 1
            else:
                j += 1


total = 0
for update in updates:
    if not check_update(update):
        correct_in_place(update)
        total += int(update[len(update) // 2])

print(total)
