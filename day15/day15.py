import time

robotMap = []
moves = []
boxes = set()
holes = set()
walls = set()
robotX = 0
robotY = 0 
robotDX = 0
robotDY = 0

directions = [ [0,-1], [1,0], [0,1], [-1,0] ]

def onMap(x, y):
    return 1 <= x < (len(robotMap[0]) - 1) and 1 <= y < (len(robotMap) -1)

def boxAhead(x, y, dx, dy):
    if (onMap(x+dx, y+dy)):
        return ( (x+dx, y+dy) in boxes )
    return False

def holeAhead(x, y, dx, dy):
    if (onMap(x+dx, y+dy)):
        return ( (x+dx,y+dy) in holes )
    return False

def wallAhead(x, y, dx, dy):

    if (x + dx == 0) or (y + dy == 0) or (x+dx == (len(robotMap[0]) - 1)) or (y+dy == (len(robotMap) - 1)):
        # external wall
        return True

    # internal walls
    if (onMap(x+dx, y+dy)):
        return ( x+dx, y+dy ) in walls

    return False

def swapBoxAndHole(boxX, boxY, holeX, holeY):
    if not (boxX, boxY) in boxes:
        print(f"ERROR: box at {boxX},{boxY} not found")

    boxes.remove( (boxX, boxY) )
    boxes.add( (holeX, holeY) )

    holes.remove( (holeX, holeY) )
    holes.add( (boxX, boxY) )

def updateMap():
    for j in range(1, len(robotMap)-1):
        for i in range(1, len(robotMap[0]) - 1):
            if ( (i, j) in boxes ):
                robotMap[j][i] = 'O'
            elif ( (i,j) in walls ):
                robotMap[j][i] = '#'
            else:
                robotMap[j][i] = '.'

    robotMap[robotY][robotX] = '@'
    
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

for j in range (0, len(robotMap)):
    for i in range(0, len(robotMap[0])):
        if (robotMap[j][i] in 'O'):
            boxes.add( (i, j) )
        elif (robotMap[j][i] in '.'):
            holes.add( (i, j) )
        elif (robotMap[j][i] == '@'):
            robotX = i
            robotY = j
        elif (robotMap[j][i] in '#') and (i >= 1 and i < len(robotMap[0]) -1) and (j >= 1 and (j < len(robotMap) - 1)):
            # internal walls
            walls.add ( (i, j) )

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

    if holeAhead(robotX, robotY, robotDX, robotDY):
        robotMap[robotY][robotX] = '.'
        holes.add( (robotX, robotY) )
        robotX += robotDX
        robotY += robotDY
    elif boxAhead(robotX, robotY, robotDX, robotDY):
        # scan in direction for next hole before wall
        x = robotX + robotDX
        y = robotY + robotDY
        hole = holeAhead(x,y,robotDX,robotDY)
        wall = wallAhead(x,y,robotDX,robotDY)
        while (not hole) and (not wall):
            x += robotDX
            y += robotDY
            hole = holeAhead(x,y,robotDX,robotDY)
            wall = wallAhead(x,y,robotDX,robotDY)

        if (hole):
           swapBoxAndHole(robotX+robotDX, robotY+robotDY,x+robotDX,y+robotDY)
           holes.add( (robotX, robotY) )
           robotX += robotDX
           robotY += robotDY

    updateMap()
    moveCount += 1

print(f"Processed {moveCount} moves")
print(f"{len(boxes)} boxes")
for r in robotMap:
    print(''.join(r))

sumGPS = 0
for b in boxes:
    sumGPS += (100 * b[1]) + b[0]

print(f"Sum of GPS {sumGPS}")
