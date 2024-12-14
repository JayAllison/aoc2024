# -----------------------------------------------------------------------------
# Day 13, Part 1
#
# Instead of a joystick or directional buttons to control the claw, these machines have two buttons
# labeled A and B. Worse, you can't just put in a token and play; it costs 3 tokens to push the
# A button and 1 token to push the B button.
#
# Each machine contains one prize; to win the prize, the claw must be positioned exactly above the
# prize on both the X and Y axes.
#
# What is the smallest number of tokens you would have to spend to win as many prizes as possible?
#
# -----------------------------------------------------------------------------

from pprint import pprint
import re


# utility function to find the lowest cost for a specific machine's A button move, B button move, and prize location
# this is not necessarily memory efficient, but because of the bounds for Part 1, that isn't a limiting factor (yet)
def find_cost(a: tuple, b: tuple, p: tuple) -> int:
    ax, ay = a
    bx, by = b
    px, py = p

    # find every possible A button press count where (A's X movement + a multiple of B's X movement) would
    # get us precisely to the prize's X pos
    # keep a list of the A button press counts that work for X
    good_x: list = []
    for i in range(101):
        if (px - (ax*i)) % bx == 0:
            good_x.append(i)

    # how many of the A X press counts also make (A's Y movement + a multiple of B's Y movement) get
    # us precisely to the prize's X pos
    # from the previous list, filter down to a list of the A button press counts that also work for Y
    good_y: list = []
    for j in good_x:
        if (py - (ay*j)) % by == 0:
            good_y.append(j)

    # now that we know each button press count that works for A, both X and Y,
    # we can check to see if the B count is the same for any of them
    # then, for all A/B button press counts that work for both X & Y, find the associated cost
    # keep a list of the costs
    costs: list = []
    for k in good_y:
        m: int = (px - (ax * k)) // bx  # calculate the number of B presses needed to make X work
        n: int = (py - (ay * k)) // by  # calculate the number of B presses needed to make Y work

        # if pressing B the same number of times makes both X and Y work, then we have found
        # both an A count and a B count that works to reach the prize - calculate the cost
        if m == n:
            costs.append(k*3 + m)
            # print(f'Press A {k} times')
            # print(f'Press B {m} times')
            # print(f'Cost = {k*3 + m} tokens')

    # return the minimum cost, if we have one
    if costs:
        return min(costs)

    # otherwise, return 0 to indicate we did not find a suitable combination
    return 0


# filename: str = 'sample.txt'
filename: str = 'input.txt'

# Parse the input:
# 1) separate the machines
machine_behaviors = open(filename).read().split('\n\n')
# a regular expression to get the digits following the letter X plus any operator; same for Y
parser = re.compile(r'.*X.(\d+).*Y.(\d+)')

# 2) extract the A, B, and prize coordinates using regex - group sequentially within the same machine
machines = []
for machine_behavior in machine_behaviors:
    machine = []
    for line in machine_behavior.split('\n'):
        if line:
            # use the regex to extract the X & Y digits
            x, y = parser.match(line).groups()
            # store these values in this machine as integers
            machine.append((int(x), int(y)))
    machines.append(machine)

# Execute the algorithm:
#  - for each machine, determine the cost (if possible)
total_cost = 0
for machine in machines:
    total_cost += find_cost(*machine)

# display the result
print(total_cost)
