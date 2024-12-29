""" AdventOfCode Day 3 """
from re import findall

totalPart1 = 0
with open("input", "r", encoding="utf-8") as f:
   for line in f.readlines():
       for a, b in findall(r"mul\((\d+),(\d+)\)", line):
           totalPart1 += int(a) * int(b)

print(f"PART1 total: {totalPart1}")
