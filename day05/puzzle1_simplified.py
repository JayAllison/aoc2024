# -----------------------------------------------------------------------------
# Day 5, Part 1:
#
# The first section specifies the page ordering rules, one per line.
#
# The second section specifies the page numbers of each update.
#
# Start by identifying which updates are already in the right order.
# -----------------------------------------------------------------------------

from collections import defaultdict

# filename: str = "sample.txt"
filename: str = "input.txt"

# break the input into the two separate sections, so that we can parse them separately
rules_section, updates_section = open(filename).read().split('\n\n')

# -----------------------------------------------------------------------------
# Parsing the rules:
# -----------------------------------------------------------------------------

# each rule in on a separate line, so we first need to separate those lines
rules_lines: list[str] = rules_section.split('\n')

# to execute this puzzle, we need to be able to answer the question, "is page X allowed before page Y"?
# note that in the rules, the left column is not unique - a page number can appear there multiple times
# in other words, one "must be before" page can have more than one "must be after" page
#
# my approach: store rules as a dict, where the key is the "must be before" page and the value is a "must be after" list
# in other words, every page in that list (the dict value) must be after the dict key
# this makes it easy to build the algoorithm below around the 'in' operator
#
# using a defaultdict instead of a standard dict just makes it easier when we're adding the first element to the list
# otherwise, we would have to check if the key already existed, and if so, we'd need to append to the list,
# but if not, we'd have to create the list and add the key & value to the dict
# defaultdict simplifies that down to a single line, assuming every value in the dict will be the same data type
rules: defaultdict = defaultdict(list)

# build up the dict by separating the page ordering requirements, which are delineated with a '|'
# we could convert these number strings to ints here, but we don't have to, so I didn't
for rule in rules_lines:
    first, second = rule.split('|')
    rules[first].append(second)

# -----------------------------------------------------------------------------
# Parsing the updates:
# -----------------------------------------------------------------------------

# this parsing is much simpler - just split each update into a list of number strings,
# and then we can process each update one by one
# we could convert these number strings to ints here, but we don't have to, so I didn't
updates: list[str] = []
for pages in updates_section.split('\n'):
    # there could be one blank line at the end - we want to skip it, so check each time that the line isn't blank
    if pages:
        separated_pages = pages.split(',')
        updates.append(separated_pages)


# -----------------------------------------------------------------------------
# decomposing the solution:
# this is a utility function to apply the ordering rules to a given update
# -----------------------------------------------------------------------------
def check_update(pages_to_update) -> bool:
    # step through the update, page by page
    for i in range(len(pages_to_update)):
        # focus on the section of the update before the current position - using a slice makes this neat and clean
        for p in pages_to_update[0:i]:
            # for the current page, if any previous page is in the "must be after" list,
            # then this update is not correctly ordered
            if p in rules[pages_to_update[i]]:
                return False

    # if we got to the end of the update and did not find an error, then the update must be correct
    return True


# -----------------------------------------------------------------------------
# the script below uses the utility function to sort out only the good updates
# so that we can then perform the summing operation specified by the puzzle
# -----------------------------------------------------------------------------

# store the correct updates in a list
good_updates = []

# check each update that we were given - if it's good, store it off
for update in updates:
    if check_update(update):
        good_updates.append(update)

# calculate the total as requested
total = 0
for good in good_updates:
    # in Python, the '//' operator does integer division (no rounding), discarding the remainder
    # for an odd-numbered list, the middle item's position = (length // 2) + 1,
    # for a zero-based array, then, the middle index = [(length // 2) + 1] + 1, which simplifies to length // 2
    total += int(good[len(good) // 2])

# display the result
print(total)
