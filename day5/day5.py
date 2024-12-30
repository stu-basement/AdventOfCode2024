""" AdventOfCode Day 5 """
import functools

rules = set()
updates = []
incorrect_updates = []
with open("input", "r", encoding="utf-8") as f:
    line = f.readline().replace('\n', '')
    while len(line) > 1:
        rules.add(tuple(map(int, line.split("|"))))
        line = f.readline().replace('\n', '')

    line = f.readline().replace('\n', '')
    while len(line) > 1:
        updates.append(list(map(int, line.split(","))))
        line = f.readline().replace('\n', '')

total_middle_number = 0
for u in updates:
    if all(list( (u0, u1) in rules for u0, u1 in zip(u, u[1:]))):
        total_middle_number += u[len(u) // 2]
    else:
        incorrect_updates.append(u)

print(f"PART1 total of middle numbers {total_middle_number}")

def compare_updates(a, b):
    """ Compare two updates using the ruleset """
    # return -1 if there is a rule that says a should be before b or
    # return 1 if there is a rule that says a should be after b otherwise
    # return 0 as pages are already correctly ordered
    return -1 if (a, b) in rules else 1 if (b, a) in rules else 0

total_middle_number = 0
for u in incorrect_updates:
    corrected = sorted(u, key=functools.cmp_to_key(compare_updates))
    total_middle_number += corrected[len(corrected) // 2]

print(f"PART2 total of middle numbers {total_middle_number}")
