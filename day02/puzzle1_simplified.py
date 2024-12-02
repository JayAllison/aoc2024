# -----------------------------------------------------------------------------
# First part of Day 2:
#
# Your puzzle input consists of many reports, one report per line.
# Each report is a list of numbers called levels that are separated by spaces.
#
# A report only counts as safe if both of the following are true:
#
#   - The levels are either all increasing or all decreasing
#   - Any two adjacent levels differ by at least one and at most three
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# decomposing our solution: check a single report against the puzzle's "safe" rules
# -----------------------------------------------------------------------------
def is_report_safe(report: list) -> bool:
    # calculate the difference between each step and the next step - save this into a list
    deltas: list[int] = []
    for i in range(len(report) - 1):
        delta = report[i] - report[i + 1]
        deltas.append(delta)

    # check if all of the differences are increasing
    all_increasing: bool = True
    for d in deltas:
        if d <= 0:  # negative numbers are not increasing; 0 is not increasing, either
            all_increasing = False
            break  # once we've found one failure, there is no need to check the rest

    # check if all of the differences are decreasing
    all_decreasing: bool = True
    for d in deltas:
        if d >= 0:  # positive numbers are not decreasing; 0 is no decreasing, either
            all_decreasing = False
            break  # once we've found one failure, there is no need to check the rest

    # first condition: must be all increasing or all decreasing - if neither, then it's not "safe"
    if not (all_increasing or all_decreasing):
        return False

    # second condition: adjacent levels must differ by at least one and at most three
    for d in deltas:
        if abs(d) < 1 or abs(d) > 3:
            return False

    # we have eliminated all of the not "safe" conditions, so this report must be "safe"
    return True


# -----------------------------------------------------------------------------
# the script below calls the function above, one line/report at a time
# -----------------------------------------------------------------------------

# filename: str = 'sample.txt'
filename: str = 'input.txt'

safe_count: int = 0

# read & process each line/report from the file
with open(filename) as file:
    for line in file:
        next_report: list[int] = []
        # split this line into separate number strings
        for number_string in line.split():
            # convert those number strings to integers
            # and save into a list for this report
            next_report.append(int(number_string))

        # using our utility function, check if this report is "safe"
        if is_report_safe(next_report):
            safe_count += 1

# display the result
print(safe_count)
