# filename: str = 'sample.txt'
filename: str = 'input.txt'

stones = [int(_stone) for _stone in open(filename).readline().rstrip().split(' ')]

repeats = 25

for _repeat in range(1, repeats + 1, 1):
    new_stones = []

    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            number = str(stone)
            first = int(number[0:len(number)//2])
            new_stones.append(first)
            second = int(number[len(number)//2:])
            new_stones.append(second)
        else:
            new_stones.append(2024 * stone)

    stones = new_stones

print(len(stones))
