# filename: str = 'sample.txt'
filename: str = 'input.txt'

# parse each line of the input file
file = open(filename)
register_a: int = int(file.readline().rstrip().split(': ')[1])
register_b: int = int(file.readline().rstrip().split(': ')[1])
register_c: int = int(file.readline().rstrip().split(': ')[1])
program: list[int] = [int(p) for p in file.read().rstrip().split(': ')[1].split(',')]

# register_a = 0
# register_b = 2024
# register_c = 43690
# program = [4,0]

# print(f'A: {register_a}')
# print(f'B: {register_b}')
# print(f'C: {register_c}')
#
# print(f'Program: {program}')


# combo operand lookup
def combo(op: int) -> int:
    # 0-3: the literal value
    if 0 <= op <= 3:
        return op
    # 4: the value in register A
    elif op == 4:
        return register_a
    # 5: the value in register B
    elif op == 5:
        return register_b
    # 6: the value in register C
    elif op == 6:
        return register_c
    # 7: not valid
    else:
        print(f'combo error! {op}')


instruction_pointer: int = 0
output: list[str] = []

while instruction_pointer < len(program):
    opcode: int = program[instruction_pointer]
    operand: int = program[instruction_pointer+1]

    # increase instruction pointer by 2 after almost every operation
    instruction_pointer += 2

    match opcode:
        case 0:  # opcode 0 (adv), integer division: A // 2 ^ combo operand -> A
            register_a = register_a // 2**combo(operand)
        case 6:  # opcode 6 (bdv), integer division: A // 2 ^ combo operand -> B
            register_b = register_a // 2**combo(operand)
        case 7:  # opcode 7 (cdv), integer division: A // 2 ^ combo operand -> C
            register_c = register_a // 2**combo(operand)
        case 1:  # opcode 1 (bxl): B XOR literal operand -> B
            register_b = register_b ^ operand
        case 2:  # opcode 2 (bst): combo operand % 8 -> B
            register_b = combo(operand) % 8
        case 3:  # opcode 3 (jnz): noop if A == 0; otherwise, jump to literal operand, do not increment
            if register_a != 0:
                instruction_pointer = operand
        case 4:  # opcode 4 (bxc): B XOR C -> B (ignore operand)
            register_b = register_b ^ register_c
        case 5:  # opcode 5 (out): combo operand % 8 -> output (comma-separated)
            output.append(str(combo(operand) % 8))

print(','.join(output))

# print(f'A: {register_a}')
# print(f'B: {register_b}')
# print(f'C: {register_c}')
