# from pprint import pprint

# filename: str = 'sample.txt'
filename: str = 'input.txt'

disk_map = open(filename).readline().rstrip()
disk = []

# fill out the files and spaces by file ID number
id_number = 0
for i in range(len(disk_map)):

    if i % 2 == 0:  # even positions indicate a file length
        disk.extend([id_number for j in range(int(disk_map[i]))])
        id_number += 1

    else:  # odd positions indicate free space
        disk.extend([None for j in range(int(disk_map[i]))])

# fold the end back onto the disk, to fill up the space - Part 1's algorithm
to_block = 0
from_block = len(disk) - 1
while True:
    while disk[to_block] is not None and to_block < len(disk):
        to_block += 1

    while disk[from_block] is None and from_block >= 0:
        from_block -= 1

    if to_block > from_block:
        break

    disk[to_block] = disk[from_block]
    disk[from_block] = None

    to_block += 1
    from_block -= 1

# calculate the checksum
checksum = 0
for i in range(len(disk)):
    if disk[i] is not None:
        checksum += i * disk[i]

print(checksum)
