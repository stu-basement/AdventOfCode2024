""" AdventOfCode Day 15 Part 2 """
moves = []
boxes = set()
walls = set()
robotX = 0
robotY = 0
robotDX = 0
robotDY = 0

def boxAheadOfRobot(x, y, dx, dy):
    """ Test if there is a box ahead of the robot in the direction of travel """
    # left/right for double-sized boxes to the left of location
    if dx != 0:
        boxX = x + dx if dx == -1 else x

        if (boxX+dx, y+dy) in boxes:
            return (boxX+dx, y+dy)

    # up/down
    if dy != 0:
        if (x+dx, y+dy) in boxes:
            return ( (x+dx, y+dy) )
        if (x+dx-1, y+dy) in boxes:
            return ( (x+dx-1, y+dy) )

    return None

def boxesAheadOfBox(b, dx, dy):
    """ Find the box ahead of x,y in the current direction dx,dy """
    # boxes can be offset +/1 if they are stacked vertically
    # Treat left/right differently to find box start offset y 1
    stackOfBoxes = []
    x = b[0]
    y = b[1]

    # left/right for double-sized boxes to the left of location
    if dx != 0:
        boxX = x + (2 * dx)

        if (boxX, y + dy) in boxes:
            stackOfBoxes.append( (boxX, y + dy) )

    # there can be multiple boxes in an up/down stack
    #
    # [][] [][] [] []   []  []   @     @
    #  []   [] []   [] []    []  []   []
    #  @     @ @    @   @     @ [][] [][]
    #
    # A box is stacked above the robot facing up if:
    # The origin of the box is inline with the robot or -1
    # A box B is stacked above a box B1 in the stack if:
    # The origin of the box B is inline with the origin of the box B1 or +/-1
    if dy != 0:
        # check inline with x+dx
        if (x+dx, y+dy) in boxes:
            stackOfBoxes.append( (x+dx, y+dy) )

        # check offset -1
        if (x+dx-1,y+dy) in boxes:
            stackOfBoxes.append( (x+dx-1, y+dy) )

        # check offset -1
        if (x+dx+1,y+dy) in boxes:
            stackOfBoxes.append( (x+dx+1, y+dy) )

    return stackOfBoxes

def wallAheadOfBox(b, dx, dy):
    """ Test to see if there is a box ahead of another box """
    # deal with all overlaps of double-width boxes
    if dx == 1:
        return (b[0] + 1 + dx, b[1] + dy) in walls

    if dx == -1:
        return (b[0] + dx, b[1] + dy) in walls

    if dy != 0:
        return (b[0] + dx, b[1] + dy) in walls or (b[0] + 1 + dx, b[1] + dy) in walls

    return None

map_height = 0
map_width = 0
with open("input", "r", encoding="utf-8") as f:
    line = f.readline().replace('\n', '')
    map_width = len(line)
    while line:
        for x, square in enumerate(list(line)):
            if square == '#':
                walls.add( (2 * x, map_height) )
                walls.add( ((2 * x) + 1, map_height) )
            elif square == 'O':
                boxes.add( (2 * x, map_height) )
            elif square == '@':
                robotX, robotY = 2 * x, map_height
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
        robotDX, robotDY = 1,0

    if m == "v":
        robotDX, robotDY = 0, 1

    if m == "<":
        robotDX, robotDY = -1, 0

    # do nothing if there is a wall ahead of the robot
    if (robotX + robotDX, robotY + robotDY) in walls:
        continue

    box = boxAheadOfRobot(robotX, robotY, robotDX, robotDY)
    if box is None:
        # move the robot into a free space
        robotX += robotDX
        robotY += robotDY
    else:
        boxStack = []

        # we might have to move a stack of boxes
        boxStack.append(box)
        visited = [box]
        toMove = []
        while boxStack:
            box = boxStack.pop()
            toMove.append(box)
            if wallAheadOfBox(box, robotDX, robotDY):
                # stack cannot move because a box at this level is blocked
                toMove = []
                break

            nextLevel = boxesAheadOfBox(box, robotDX, robotDY)
            for box in nextLevel:
                if box not in visited:
                    visited.append(box)
                    boxStack.append( box )

        if toMove:
            # Move robot into gap
            robotX += robotDX
            robotY += robotDY
        while toMove:
            box = toMove.pop()
            boxes.remove( (box[0], box[1]) )
            boxes.add( (box[0] + robotDX, box[1] + robotDY) )

sumGPS = sum( (100 * b[1]) + b[0] for b in boxes )
print(f"PART2: Sum of GPS {sumGPS}")
