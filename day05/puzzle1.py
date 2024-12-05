from collections import defaultdict

# filename = "sample.txt"
filename = "input.txt"

rules_section, updates_section = open(filename).read().split('\n\n')

rules = defaultdict(list)
for rule in rules_section.split('\n'):
    first, second = rule.split('|')
    rules[first].append(second)

updates = [pages.split(',') for pages in updates_section.split('\n') if pages]


def check_update(pages_to_update) -> bool:
    # is this too compact??? ;)
    return all([p not in rules[pages_to_update[i]] for i in range(len(pages_to_update)) for p in pages_to_update[0:i]])


centers = [int(update[len(update) // 2]) for update in updates if check_update(update)]
print(sum(centers))
