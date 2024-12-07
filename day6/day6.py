import time

areaMap = []
visited = []

def onMap(x, y):
    return (x >= 0) and (x < len(areaMap[0]) - 1) and (y >=0) and (y < len(areaMap))

def obstacleAhead(x,y,deltaX,deltaY):
    if onMap(x+deltaX,y+deltaY):
        return areaMap[y + deltaY][x + deltaX] == '#' or areaMap[y + deltaY][x + deltaX] == 'O'
    return False

def visit(x, y, dx, dy):
    # Look for existing visit record
    for v in visited:
        if (v[0] == x and 
            v[1] == y and 
            v[2] == dx and 
            v[3] == dy):
            v[4] += 1  # increment visit count
      #      print(f"Visted {x},{y},{dx},{dy} {v[4]+1} times")
            return
            
    # First time visiting this state
    visited.append([x, y, dx, dy, 1])
    # print(f"First time at {x},{y},{dx},{dy}")

def placeObstacle(x, y):
    row = areaMap[y]
    areaMap[y] = row[:x] + 'O' + row[x+1:]

def detectLoop(x, y, dx, dy):
    # A loop exists if:
    # 1. We've been at this exact position and direction before
    # 2. We've visited it more than once (2 times is enough for a loop)
    for v in visited:
        if (v[0] == x and 
            v[1] == y and 
            v[2] == dx and 
            v[3] == dy and 
            v[4] > 1):  # changed from > 1 to >= 2 if needed
            # print(f"Loop detected at {x},{y},{dx},{dy} after {v[4]} visits")
            return True
            
    return False

def traverseMap(startX, startY, skipToX=None, skipToY=None, skipToDx=None, skipToDy=None):
    if skipToX is not None:
        # Follow the original path up to the obstacle point
        for v in part1Visited:
            if v[0] == skipToX and v[1] == skipToY:
                break
            visit(v[0], v[1], v[2], v[3])
        
        guardX = skipToX
        guardY = skipToY
        guardDeltaX = skipToDx
        guardDeltaY = skipToDy
    else:
        guardX = startX
        guardY = startY
        guardDeltaX = 0
        guardDeltaY = -1
    
    while onMap(guardX, guardY):
        visit(guardX, guardY, guardDeltaX, guardDeltaY)
        
        if detectLoop(guardX, guardY, guardDeltaX, guardDeltaY):
            return True
            
        # Get next position
        nextX = guardX + guardDeltaX
        nextY = guardY + guardDeltaY
        
        if obstacleAhead(guardX, guardY, guardDeltaX, guardDeltaY):
            # Turn right
            if guardDeltaX == 0:
                if guardDeltaY == -1:
                    guardDeltaX = 1
                    guardDeltaY = 0
                else:
                    guardDeltaX = -1
                    guardDeltaY = 0
            else:
                if guardDeltaX == -1:
                    guardDeltaX = 0
                    guardDeltaY = -1
                else:
                    guardDeltaX = 0
                    guardDeltaY = 1
        else:
            # Move forward
            guardX = nextX
            guardY = nextY
    
    return False

# Test part 1 with the sample input
print("PART 1 - Sample input")
with open("sampleinput", "r") as f:
    for line in f.readlines():
        areaMap.append(line)

originalMap = areaMap.copy()
for l in range(0, len(areaMap)):
    for m in range(0, len(areaMap[0])):
        if areaMap[l][m] == '^':
            startX = m
            startY = l
areaMap = originalMap.copy()
visited = []
loopDetected = traverseMap(startX, startY)   
visitedCount = 0
visited_positions = set()  # Use a set to track unique positions

for v in visited:
    pos = (v[0], v[1])  # Just use x,y coordinates
    if pos not in visited_positions:  # Only count if we haven't seen this position
        visited_positions.add(pos)
        if areaMap[v[1]][v[0]] != 'X':
            areaMap[v[1]] = areaMap[v[1]][:v[0]] + "X" + areaMap[v[1]][v[0]+1:]
            visitedCount += 1

print("VISITED")
for row in areaMap:
    print(row)
print(visited)
print(f"Sample input visited {visitedCount}")

areaMap = []
with open("input", "r") as f:
    for line in f.readlines():
        areaMap.append(line)
originalMap = areaMap.copy()

print(f"Starting map width {len(areaMap[0])} height {len(areaMap)}")
for row in originalMap:
    print(row)

print("Part 1 - no loops should be detected")
for l in range(0, len(areaMap)):
    for m in range(0, len(areaMap[0])):
        if areaMap[l][m] == '^':
            startX = m
            startY = l
loopDetected = traverseMap(startX, startY)
print(f"Loop detected: {loopDetected}")

visitedCount = 0
for v in visited:
    if areaMap[v[1]][v[0]] != 'X':
        areaMap[v[1]] = areaMap[v[1]][:v[0]] + "X" + areaMap[v[1]][v[0]+1:]
        visitedCount += 1
print("VISITED")
for row in areaMap:
    print(row)
print(visited)
part1Visited = visited.copy()
print(f"Part 1 input visited {visitedCount}")

print("Part 2 - try to cause loops by placing obstructions")
loopCount = 0
testCount = 0
unique_positions = set()
print(f"PART 2 - try {len(part1Visited)} locations")
for v in part1Visited:
    unique_positions.add((v[0], v[1]))

for i, v in enumerate(part1Visited):
    x, y = v[0], v[1]
    visited = []
    if originalMap[y][x] == '.' and not (x == startX and y == startY and originalMap[y][x] == '.'):
        testCount += 1
        areaMap[y]=areaMap[y][:x]+'O'+areaMap[y][x+1:]

        # Time the path calculation
        path_start = time.time()
        prev_state = part1Visited[i-1] if i > 0 else None
        if prev_state:
            loopDetected = traverseMap(startX, startY, x, y, prev_state[2], prev_state[3])
        else:
            loopDetected = traverseMap(startX, startY)
        path_time = time.time() - path_start

        if loopDetected:
            print(f"Placing obstacle at {x},{y} has caused loop #{loopCount+1}")
            loopCount += 1
        areaMap[y]=areaMap[y][:x]+originalMap[y][x]+areaMap[y][x+1:]        

print(f"Part 1 unique positions {len(unique_positions)}")
print(f"Loops detected {loopCount}")
print(f"Tested {testCount}")
