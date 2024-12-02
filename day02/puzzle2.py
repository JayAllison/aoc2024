# filename: str = 'sample.txt'
filename: str = 'input.txt'


def is_report_safe(report: list) -> bool:
    diffs = [report[i] - report[i+1] for i in range(len(report)-1)]

    positives = [d > 0 for d in diffs]
    negatives = [d < 0 for d in diffs]
    adjacents = [1 <= abs(d) <= 3 for d in diffs]

    if not all(positives) and not all(negatives):
        return False

    return all(adjacents)


def is_report_safe_in_any_way(report: list) -> bool:
    if is_report_safe(report):
        return True

    length = len(report)
    alternates = [is_report_safe(report[0:i] + report[i+1:length]) for i in range(length)]

    return any(alternates)


reports = [[int(x) for x in line.rstrip().split()] for line in open(filename)]

safe_count = [is_report_safe_in_any_way(lev) for lev in reports].count(True)

print(safe_count)
