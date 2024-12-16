import time

robotMap = []
moves = []
boxes = set()
walls = set()
robotX = 0
robotY = 0 
robotDX = 0
robotDY = 0

directions = [ [0,-1], [1,0], [0,1], [-1,0] ]

def onMap(m, x, y):
    return 1 <= x < (len(m[0]) - 1) and 1 <= y < (len(m) -1)

def boxAheadOfRobot(m, x, y, dx, dy):

    # left/right for double-sized boxes to the left of location
    if (dx == 1 or dx == -1):
        if (dx == -1):
            boxX = x-1
        elif (dx == 1):
            boxX = x

        if (boxX+dx, y+dy) in boxes:
            return (boxX+dx, y+dy)

    if (dy == 1 or dy == -1):
        if ( (x+dx, y+dy) in boxes):
            return ( (x+dx, y+dy) )
        if ( (x+dx-1, y+dy) in boxes):
            return ( (x+dx-1, y+dy) )

    return None

def boxesOverlap(b, b1):
    if (b[0] == b1[0]):
        return True
    if (b[0] == b1[0] - 1):
        return True
    if (b[0] == b1[0] +1):
        return True

    return False

def boxesAheadOfBox(m, b, dx, dy):
    # Find the box ahead of x,y in the current direction dx,dy
    # boxes can be offset +/1 if they are stacked vertically
    # Treat left/right differently to find box start offset y 1
    stackOfBoxes = []
    x = b[0]
    y = b[1]

    # left/right for double-sized boxes to the left of location
    if (dx == 1 or dx == -1):
        boxX = x+(2 * dx)

        if onMap(m, boxX, y+dy):
            if (boxX, y+dy) in boxes:
                stackOfBoxes.append( (boxX, y+dy) )

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
    if (dy == 1 or dy == -1):
        # check inline with x+dx
        if onMap(m, x+dx, y+dy):
            if (x+dx, y+dy) in boxes:
                stackOfBoxes.append( (x+dx, y+dy) )

        # check offset -1
        if onMap(m, x+dx-1, y+dy):
            if (x+dx-1,y+dy) in boxes:
                stackOfBoxes.append( (x+dx-1, y+dy) )

        # check offset -1
        if onMap(m, x+dx+1, y+dy):
            if (x+dx+1,y+dy) in boxes:
                stackOfBoxes.append( (x+dx+1, y+dy) )

    return stackOfBoxes

def wallAhead(m, x, y, dx, dy):
    if (x + dx == 0) or (y + dy == 0) or (x+dx == (len(robotMap[0]) - 1)) or (y+dy == (len(robotMap) - 1)):
        # external wall
        return True

    # internal walls
    if (onMap(m, x+dx, y+dy)):
        return ( x+dx, y+dy ) in walls

    return False

def wallAheadOfBox(m, b, dx, dy):
    if ( dx == 1):
        return wallAhead(m, b[0]+1, b[1], dx, dy)
    elif (dx == -1):
        return wallAhead(m, b[0], b[1], dx, dy)

    if ( dy == -1 or dy == 1):
        return wallAhead(m, b[0], b[1], dx, dy) or wallAhead(m, b[0]+1, b[1], dx, dy)

def moveBox(boxX, boxY, dx, dy):
    print(f"Move box at {boxX},{boxY} by {dx},{dy}")
    boxes.remove( (boxX, boxY) )
    boxes.add( (boxX+dx, boxY+dy) )

def updateMap(m):
    width = len(m[0])
    height = len(m)

    for j in range(1, height-1):
        for i in range(1, width - 1):
            m[j][i] = '.'

    for j in range(1, height-1):
        for i in range(1, width - 1):
            if ( (i, j) in boxes ):
                m[j][i] = '['
                m[j][i+1] = ']'
            elif ( (i,j) in walls ):
                m[j][i] = '#'

    m[robotY][robotX] = '@'

    return m

def expandMap(m):
    print(f"Expand map {len(m[0])} x {len(m)}")
    width = len(m[0])
    height = len(m)

    # add the new internal walls created by expanding the map
    for j in range(1, height - 1):
        walls.add ( (1, j) )
        walls.add ( ( width - 2, j) )

    return m
    
with open("input", "r") as f:
    line = f.readline()
    while (len(line) > 1):
        robotMap.append(list(line.replace('\n', '')))
        line = f.readline()

    l = f.readline()
    movesInput = ''
    while (len(l) > 1):
        movesInput += l.replace('\n','')
        l = f.readline()

moves = list(movesInput)

# start with an empty map full of holes between the outer walls
newMap = []
newMap.append(list(''.ljust(len(robotMap[0] *2), '#')))
for r in range(1, len(robotMap) - 1):
    newMap.append( list( '#' + ''.ljust(2 * (len(robotMap[0]) - 1), ' ')+"#" ) )
newMap.append(list(''.ljust(len(robotMap[0] * 2), '#')))
for r in newMap:
    print(''.join(r))

for j in range (0, len(robotMap)):
    for i in range(0, len(robotMap[0])):
        if (robotMap[j][i] in 'O'):
            boxes.add( ( (i * 2),j) )
        elif (robotMap[j][i] == '@'):
            robotX = i * 2
            robotY = j
        elif (robotMap[j][i] in '#') and (i >= 1 and i < len(robotMap[0]) -1) and (j >= 1 and (j < len(robotMap) - 1)):
            # internal walls
            walls.add ( ( (i * 2), j) )
            walls.add ( ( (i * 2) + 1, j) )

print(boxes)

robotMap = expandMap(newMap)
robotMap = updateMap(robotMap)
for r in robotMap:
    print(''.join(r))

print(f"Map {len(robotMap[0])} x {len(robotMap)}")
print(f"{len(moves)} moves")
print(f"{len(boxes)} boxes")
for r in robotMap:
    print(''.join(r))

print(f"Robot start at {robotX},{robotY}")

print(f"Number of moves: {len(moves)}")
moveCount = 0
for m in moves:
    if (m == "^"):
        robotDX = 0
        robotDY = -1

    if (m == ">"):
        robotDX = 1
        robotDY = 0

    if (m == "v"):
        robotDX = 0
        robotDY = 1

    if (m == "<"):
        robotDX = -1
        robotDY = 0

    robotMap = updateMap(robotMap)
    for r in robotMap:
        print(''.join(r))
    print(f"Move {m} robot at {robotX},{robotY}")
#    input()

    robotCanMove = not (wallAhead(robotMap, robotX, robotY, robotDX, robotDY) or boxAheadOfRobot(robotMap, robotX, robotY, robotDX, robotDY))
    if robotCanMove:
        robotX += robotDX
        robotY += robotDY
    elif not wallAhead(robotMap, robotX, robotY, robotDX, robotDY):
        boxStack = []
        print(f"No hole ahead of robot - scan for walls and boxes from {robotX},{robotY} by {robotDX},{robotDY}")
        b = boxAheadOfRobot(robotMap, robotX, robotY, robotDX, robotDY)
        if (b == None):
            print(f"ERROR: No box found when should have been")
            exit()

        print(f"Box {b[0]},{b[1]} is first in stack")

        # we might have to move a stack of boxes 
        boxStack.append(b)
        visited = [b]
        toMove = []
        while len(boxStack) > 0:
            b = boxStack.pop()
            toMove.append(b)
            if wallAheadOfBox(robotMap, b, robotDX, robotDY):
                # stack cannot move because a box at this level is blocked
                print(f"Stack of boxes cannot move {boxStack} because {b} is blocked")
                toMove = []
                break

            nextLevel = boxesAheadOfBox(robotMap, b, robotDX, robotDY)
            for b in nextLevel:
                print(f"Add box {b} to stack")
                if b not in visited:
                    print(f"Add box {b} to visited")
                    visited.append(b)
                    boxStack.append( b )

        print(f"Moving a stack of boxes {toMove} visited {visited}")
        if len(toMove) > 0:
            # Move robot into gap
            robotX += robotDX
            robotY += robotDY
        while len(toMove) > 0:
            b = toMove.pop()
            moveBox(b[0], b[1], robotDX, robotDY)


    moveCount += 1

print(f"Processed {moveCount} moves")
print(f"{len(boxes)} boxes")
robotMap = updateMap(robotMap)
for r in robotMap:
    print(''.join(r))

sumGPS = 0
for b in boxes:
    sumGPS += (100 * b[1]) + b[0]

print(f"Sum of GPS {sumGPS}")
