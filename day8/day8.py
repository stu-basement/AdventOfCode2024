""" AdventOfCode Day 8 """
from collections import defaultdict
import itertools

antinode_locations = set()

# Antennas - key: antenna frequency, values:  [(X, Y)]
antennas = defaultdict()

# PART 1
map_width = 0
map_height = 0
with open("input", "r", encoding="utf-8") as f:
    line = f.readline().replace('\n', '')
    map_width = len(line)
    while line:
        for n, square in enumerate(line):
            if square != '.':
                if square in antennas:
                    antennas[square].append( (n, map_height) )
                else:
                    antennas[square] = [ (n, map_height) ]
        map_height += 1
        line = f.readline().replace('\n', '')

for _, locations in antennas.items():
    pairs = list(itertools.combinations(locations, 2))
    for x,y in [(2*a[0]-b[0], 2*a[1]-b[1]) for a,b in pairs]:
        if 0 <= x < map_width and 0 <= y < map_height:
            antinode_locations.add( (x, y) )
    for x,y in [(2*b[0]-a[0], 2*b[1]-a[1]) for a,b in pairs]:
        if 0 <= x < map_width and 0 <= y < map_height:
            antinode_locations.add( (x, y) )

print(f"PART1: Number of antinodes {len(antinode_locations)}")

antinode_locations = set()
for _, locations in antennas.items():
    pairs = list(itertools.combinations(locations, 2))
    for x, y, dx, dy in [( a[0], a[1], (b[0] - a[0]), (b[1] - a[1]) ) for a, b in pairs]:
        while 0 <= x < map_width and 0 <= y < map_height:
            antinode_locations.add( (x, y) )
            x, y = x+dx, y+dy

    for x, y, dx, dy in [( b[0], b[1], (b[0] - a[0]), (b[1] - a[1]) ) for a, b in pairs]:
        while 0 <= x < map_width and 0 <= y < map_height:
            antinode_locations.add( (x, y) )
            x, y = x-dx, y-dy
print(f"PART2: Number of antinodes {len(antinode_locations)}")
