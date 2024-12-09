from datetime import datetime
from typing import Sequence


def parse_input(filename: str) -> Sequence:  # could be list or str, depending on how I'm feeling ;)
    return open(filename).readline().rstrip()


def populate_disk(disk_map: Sequence) -> tuple[list, dict]:
    disk = []  # because we are indexing and changing but not inserting or deleting, list is fast enough
    file_sizes = {}
    id_number = 0

    # using the puzzle rules, populate the disk blocks with IDs
    for i in range(len(disk_map)):
        if i % 2 == 0:  # even positions indicate a file length
            file_sizes[id_number] = int(disk_map[i])
            disk.extend([id_number for _j in range(int(disk_map[i]))])
            id_number += 1
        else:  # odd positions indicate free space
            disk.extend([None for _j in range(int(disk_map[i]))])

    return disk, file_sizes


def find_preceding_file(disk, file_pos) -> int or None:
    # search backwards to find the tail of the next file
    while disk[file_pos] is None and file_pos >= 0:
        file_pos -= 1

    # if we got all the way back to the beginning of the disk, stop
    if file_pos <= 0:
        return None

    return file_pos


def find_suitable_opening(disk, file_pos, file_size) -> int or None:
    # find a spot to place this file
    opening_start = 0
    opening_end = None

    while True:
        # find the next blank spot
        while opening_start < len(disk) and disk[opening_start] is not None:
            opening_start += 1

        # if we got past the location of the current file, stop
        # or, if we got all the way to the end of the disk, stop
        if opening_start > file_pos or opening_start >= len(disk):
            break

        # find the end of this blank spot, which might be the end of the disk
        opening_end = opening_start
        while opening_end < len(disk) and disk[opening_end] is None:
            opening_end += 1

        # is this spot big enough?
        if opening_end - opening_start >= file_size:
            break

        # if not, go to the next one
        opening_start = opening_end

    # a suitable opening is long enough for the file AND before the file's current location
    if opening_end and opening_end - opening_start >= file_size and opening_start < file_pos - file_size:
        return opening_start

    return None


def move_file(disk, old_file_pos, new_file_pos, file_length, file_id):
    stopping_point = new_file_pos + file_length

    # remove the file from its current location
    for k in range(old_file_pos, old_file_pos - file_length, -1):
        disk[k] = None

    # put the new file in its new location
    while new_file_pos < stopping_point:
        disk[new_file_pos] = file_id
        new_file_pos += 1


def consolidate_files(disk, file_sizes) -> None:

    # start searching at the end
    from_block = len(disk) - 1

    while True:
        # search backwards to find the tail of the next file
        from_block = find_preceding_file(disk, from_block)

        # if we got all the way back to the beginning, stop
        if from_block is None:
            break

        # how long is the file we just found?
        id_to_move = disk[from_block]
        file_length = file_sizes[id_to_move]

        opening_block = find_suitable_opening(disk, from_block, file_length)

        # did we find a spot that is big enough that is before the current location?
        if opening_block:
            move_file(disk, from_block, opening_block, file_length, id_to_move)

        # move our marker to before the file we just found - this is where we will pick up next iteration
        from_block -= file_length


def calculate_checksum(disk) -> int:
    checksum = 0
    for i in range(len(disk)):
        if disk[i] is not None:
            checksum += i * disk[i]
    return checksum


def main():
    before = datetime.now()
    print(f'Started at {before}')

    # filename: str = 'sample.txt'
    filename: str = 'input.txt'

    disk_map = parse_input(filename)
    disk, file_sizes = populate_disk(disk_map)
    consolidate_files(disk, file_sizes)
    checksum = calculate_checksum(disk)

    print(f'Finished after {datetime.now() - before}')
    print(checksum)


if __name__ == '__main__':
    main()
