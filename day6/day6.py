""" AdventOfCode Day 6 """
# PART 1
obstacles = set()
map_height = 0
map_width = 0
guard = (0, 0, 0, -1)
with open("input", "r", encoding="utf-8") as f:
    for line in f.readlines():
        map_width = len(line) - 1
        for n, square in enumerate(line.replace('\n', '')):
            if square == '#':
                obstacles.add( (n, map_height) )
            elif square == '^':
                guard = (n, map_height, 0, -1)
        map_height += 1

visited = set()
original_guard = guard
while 0 <= guard[0] < map_width and 0 <= guard[1] < map_height:
    if (guard[0] + guard[2], guard[1] + guard[3]) in obstacles:
        # turn right at obstacle
        guard = (guard[0], guard[1], -guard[3], guard[2])
    else:
        if (guard[0], guard[1]) not in visited:
            visited.add( (guard[0], guard[1]) )
        # move forward
        guard = (guard[0] + guard[2], guard[1] + guard[3], guard[2], guard[3])
print(f"PART1 total visited {len(visited)}")

loopCount = 0
# only place obstacles at locations the guard previously visited
for v in visited:
    guard = original_guard
    unique_positions = set()
    obstacles.add( (v[0], v[1]) )

    # See if the guard goes into a loop
    while 0 <= guard[0] < map_width and 0 <= guard[1] < map_height:
        if (guard[0] + guard[2], guard[1] + guard[3]) in obstacles:
            # turn right at obstacle
            guard = (guard[0], guard[1], -guard[3], guard[2])
        else:
            # move forward
            guard = (guard[0] + guard[2], guard[1] + guard[3], guard[2], guard[3])

        if guard not in unique_positions:
            unique_positions.add( guard )
        else:
            loopCount += 1
            break
    obstacles.remove( (v[0], v[1]) )
    guard = (v[0], v[1], guard[2], guard[3])

print(f"PART2 number of loops detected {loopCount}")
