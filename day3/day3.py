""" AdventOfCode Day 3 """
from re import findall

totalPart1 = 0
totalPart2 = 0
enabled = True
with open("input", "r", encoding="utf-8") as f:
    for line in f.readlines():
        for a, b, do, dont in findall(r"mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))", line):
            if do or dont:
                enabled = bool(do)
            else:
                totalPart1 += int(a) * int(b)
                if enabled:
                    totalPart2 += int(a) * int(b)

print(f"PART1 total: {totalPart1}")
print(f"PART2 total: {totalPart2}")
