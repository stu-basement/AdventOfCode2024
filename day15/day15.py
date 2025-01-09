""" AdventOfCode Day 15 """
boxes = set()
walls = set()
robotX = 0
robotY = 0 
robotDX = 0
robotDY = 0

map_height = 0
with open("input", "r", encoding="utf-8") as f:
    line = f.readline().replace('\n', '')
    map_width = len(line)
    while line:
        for x, square in enumerate(list(line)):
            if square == '#':
                walls.add( (x, map_height) )
            elif square == 'O':
                boxes.add( (x, map_height) )
            elif square == '@':
                robotX, robotY = x, map_height
        line = f.readline().replace('\n', '')
        map_height += 1

    line = f.readline().replace('\n', '')
    moves = line
    while line:
        line = f.readline().replace('\n', '')
        moves += line

for m in moves:
    if m == "^":
        robotDX, robotDY = 0, -1

    if m == ">":
        robotDX, robotDY = 1, 0

    if m == "v":
        robotDX, robotDY = 0, 1

    if m == "<":
        robotDX, robotDY = -1, 0

    # do nothing if the robot would hit a wall
    if (robotX + robotDX, robotY + robotDY) in walls:
        continue

    # if there isn't a box next to the robot in this direction, move the robot
    if (robotX + robotDX, robotY + robotDY) not in boxes:
        robotX += robotDX
        robotY += robotDY
    else:
        # scan in current direction for a hole before wall - if found the boxes can move
        x = robotX + robotDX
        y = robotY + robotDY
        while (x + robotDX, y + robotDY) in boxes:
            x += robotDX
            y += robotDY

        if (x + robotDX, y + robotDY) not in walls:
            # box next to robot can move into this hole
            boxes.remove( (robotX + robotDX, robotY + robotDY) )
            robotX += robotDX
            robotY += robotDY
            boxes.add( (x + robotDX, y + robotDY) )

# calculate GPS result based on final position of boxes
sumGPS = sum( (100 * b[1] + b[0]) for b in boxes)
print(f"PART1: Sum of GPS {sumGPS}")
