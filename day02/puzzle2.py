# filename: str = 'sample.txt'
filename: str = 'input.txt'


def is_level_safe(level: list) -> bool:
    diffs = [level[i] - level[i+1] for i in range(len(level)-1)]

    positives = [d > 0 for d in diffs]
    negatives = [d < 0 for d in diffs]
    adjacents = [1 <= abs(d) <= 3 for d in diffs]

    if not all(positives) and not all(negatives):
        return False

    return all(adjacents)


def is_level_safe_in_any_way(level: list) -> bool:
    if is_level_safe(level):
        return True

    length = len(level)
    alternates = [is_level_safe(level[0:i] + level[i+1:length]) for i in range(length)]

    return any(alternates)


levels = [[int(x) for x in line.rstrip().split()] for line in open(filename)]

safe_count = [is_level_safe_in_any_way(lev) for lev in levels].count(True)

print(safe_count)
