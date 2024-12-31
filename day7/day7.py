""" AdventOfCode Day 7 """
import itertools
import math

results = []
values = []
operations = []
success = []

def operatorCombo(op, n):
    """ Return the combinations of all operands for the number of terms """
    yield from itertools.product(*([op] * n))

def calc(op, term1, term2):
    """ Perform the calculation term1 op term2 """
    if op == "+":
        return term1 + term2

    if op == "*":
        return term1 * term2

    if op == '|':
        return (term1 * (10 ** (math.floor(math.log10(term2)) + 1))) + term2

    return None

equations = []
with open('input', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        x = line.replace('\n', '').split(':')
        equations.append( (int(x[0]), list(map(int, x[1].split()))) )

calibration_result = 0
for e in equations:
    for combo in operatorCombo('+*', len(e[1])):
        result = e[1][0]
        for t in enumerate(e[1][1:]):
            result = calc(combo[t[0]-1], result, t[1])

        if result == e[0]:
            calibration_result += e[0]
            break
print(f"PART1 total calibration result {calibration_result}")

calibration_result = 0
for e in equations:
    for combo in operatorCombo('+*|', len(e[1])):
        result = e[1][0]

        for t in enumerate(e[1][1:]):
            result = calc(combo[t[0]-1], result, t[1])

            # Early exit if we exceed the expected result before using all the terms
            if result > e[0]:
                break

        if result == e[0]:
            calibration_result += e[0]
            break

print(f"PART2 total calibration result {calibration_result}")
