# -----------------------------------------------------------------------------
# Day 9, Part 1
#
# The disk map uses a dense format to represent the layout of files and free space on the disk.
# The digits alternate between indicating the length of a file and the length of free space.
#
# Move file blocks one at a time from the end of the disk to the leftmost free space block
# (until there are no gaps remaining between file blocks).
#
# The final step of this file-compacting process is to update the filesystem checksum.
# To calculate the checksum, add up the result of multiplying each of these blocks'
# position with the file ID number it contains.
#
# -----------------------------------------------------------------------------

filename: str = 'sample.txt'
# filename: str = 'input.txt'

# the input is a single line - we are just going to iterate over it, so leaving it as a string is fine
disk_map: str = open(filename).readline().rstrip()

# fill out the disk with file ID number for the length of each file, with the specified spaces in between
# using a list to represent the disk of file blocks until performance dictates that we need something different
disk: list[int | None] = []
id_number: int = 0
for map_index in range(len(disk_map)):
    map_value: int = int(disk_map[map_index])
    # even positions in the map indicate a file length - take advantage of list's * operator
    if map_index % 2 == 0:
        # fill out the entire size of the file with the file's ID - take advantage of list's * operator
        disk.extend([id_number] * map_value)
        id_number += 1
    # odd positions in the map indicate free space length
    else:
        # using None as a placeholder for free space
        disk.extend([None] * map_value)

# fold the end back onto the disk, to fill up the space - Part 1's algorithm is much simpler than Part 2's

to_block: int = 0  # index of the first empty space
from_block: int = len(disk) - 1  # index of a file block

while True:
    # search the disk forward to find an empty block
    while disk[to_block] is not None:
        to_block += 1

    # search the disk backwards to find a non-empty block
    while disk[from_block] is None:
        from_block -= 1

    # when our searches pass each other, we are done - there is no more free space to fill up
    if to_block > from_block:
        break

    # move the file block from the old location to the new location
    disk[to_block] = disk[from_block]
    disk[from_block] = None

    # advance both searches and go again
    to_block += 1
    from_block -= 1

# calculate the checksum, per the puzzle rule
checksum: int = 0
for i in range(len(disk)):
    if disk[i] is not None:
        checksum += i * disk[i]

# display the output
print(checksum)
