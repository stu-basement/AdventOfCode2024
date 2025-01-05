""" AdventOfCode Day 17 """
def getCombo(op, regA, regB, regC):
    """ Return the value of a combo operand """
    return op if (op <= 3) else regA if op == 4 else regB if op == 5 else regC if op == 6 else None

def executeProgram(p, regA, regB, regC):
    """ Simulate the execution of the program """
    pc = 0
    output = []
    while pc < len(p):
        instruction = p[pc]
        operand = p[pc + 1]
        if instruction == 0:
            regA >>= getCombo(operand, regA, regB, regC)
        elif instruction == 1:
            regB ^= operand
        elif instruction == 2:
            regB = getCombo(operand, regA, regB, regC) % 8
        elif instruction == 3:
            pc = operand if regA else pc + 2
        elif instruction == 4:
            regB ^= regC
        elif instruction == 5:
            output.append(getCombo(operand, regA, regB, regC) % 8)
        elif instruction == 6:
            regB = regA >> getCombo(operand, regA, regB, regC)
        elif instruction == 7:
            regC = regA >> getCombo(operand, regA, regB, regC)

        # we have already adjusted program counter for the jump instruction
        if instruction != 3:
            pc += 2

    return output

with open("input", "r", encoding="utf-8") as f:
    line = f.readline()
    aRegister = int(line.split(':')[1])
    line = f.readline()
    bRegister = int(line.split(':')[1])
    line = f.readline()
    cRegister = int(line.split(':')[1])

    line = f.readline()
    program = list( map(int, f.readline().split(":")[1].split(",")))

program_output = executeProgram(program, aRegister, bRegister, cRegister)
print("PART1: ", program_output)

# DFS through the program search space
# at each digit of the output, there are one or more programs that produce that output
# at the top level (all the digits of the output), we want the lowest program value
# that produces the full output
aRegister = 0
visited = {0}
for digit in reversed(program):
    next_a = set()

    for a in visited:
        aRegister = a * 8

        for i in range(8):
            program_output = executeProgram(program, aRegister + i, 0, 0)
            if program_output[0] == digit:
                next_a.add( aRegister + i )
        visited = next_a

    aRegister = min(visited)

result = executeProgram(program, aRegister, 0, 0)
print(f"PART2: {aRegister}")
