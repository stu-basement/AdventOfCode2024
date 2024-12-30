""" AdventOfCode Day 4 """
from collections import defaultdict

xmas = ['X', 'M', 'A', 'S']
directions = [ -1, 0, 1 ]

letter_spots = defaultdict()
x_spots = set()
a_spots = set()

y = 0
with open("input", "r", encoding="utf-8") as f:
    line = list(f.readline().replace('\n', ''))
    while len(line) > 0:
        for x, l in enumerate(line):
            if l == 'X':
                x_spots.add( (x, y) )

            if l == 'A':
                a_spots.add( (x, y) )

            if l != '.':
                letter_spots[(x, y)] = l

        line = list(f.readline().replace('\n', ''))
        y += 1

foundCount = 0
for x, y in x_spots:
    for dx in directions:
        for dy in directions:
            matched = 0
            for n, l in enumerate(xmas):
                if (x + (dx * n), y + (dy * n)) in letter_spots:
                    matched += letter_spots[ (x + (dx * n), y + (dy * n)) ] == l

            if matched == len(xmas):
                foundCount += 1

print(f"PART1: total found {foundCount}")

foundCount = 0
for x, y in a_spots:
    if  (x - 1, y - 1) in letter_spots and (x + 1, y - 1) in letter_spots and \
            (x - 1, y + 1) in letter_spots and (x + 1, y + 1) in letter_spots:
        top = letter_spots[ (x - 1, y - 1)] + letter_spots[ (x + 1, y - 1) ]
        bottom = letter_spots[ (x - 1, y + 1) ] + letter_spots[ (x + 1, y + 1) ]

        if (top in 'SS' and bottom in 'MM') or (top in 'MS' and bottom in 'MS') \
                or (top in 'SM' and bottom in 'SM') or (top in 'MM' and bottom in 'SS'):
            foundCount += 1

print(f"PART2: total found (part 2): {foundCount}") 

