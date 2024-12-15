MAP_WIDTH = int(101)
MAP_HEIGHT = int(103)

robotMap = []
startPoints = []
velocities = []
currentPositions = []

def calcSafetyFactor():
    quadBR = 0
    quadBL = 0
    quadUL = 0
    quadUR = 0
    for p in currentPositions:
       if (p[1] == MAP_HEIGHT // 2) or (p[0] == MAP_WIDTH // 2):
           continue

       if (p[1] < MAP_HEIGHT // 2) and (p[0] < MAP_WIDTH // 2):
           quadUL += 1 

       if (p[1] < MAP_HEIGHT // 2) and (p[0] >= MAP_WIDTH // 2):
           quadUR += 1

       if (p[1] >= MAP_HEIGHT // 2) and (p[0] >= MAP_WIDTH // 2):
           quadBR += 1

       if (p[1] >= MAP_HEIGHT // 2) and (p[0] < MAP_WIDTH // 2):
           quadBL += 1

    return quadUL * quadUR * quadBL * quadBR

def distanceFromCentre():
    totalDistance = 0
    for p in currentPositions:
        totalDistance += abs(p[0] - (MAP_WIDTH //2)) + abs(p[1] - (MAP_HEIGHT // 2))
    return totalDistance

def placeRobot(x, y):
    n = robotMap[y][x]
    if (n == '.'):
        robotMap[y][x] = str(1)
    else:
        robotMap[y][x] = str(int(n)+1)

def moveRobot(x, y, newX, newY):
    # Move robot from old location
    n = robotMap[y][x]
    robotMap[y][x] = str(int(n)-1) if (int(n)-1 > 0) else '.'

    # Update new location after moving
    placeRobot(newX, newY)

def updatePositionsAtTime(t):
    for p in range(0, len(currentPositions)):
        x = currentPositions[p][0]
        y = currentPositions[p][1]
        dx = velocities[p][0]
        dy = velocities[p][1]

        if (t > 0):
            currentPositions[p][0] = (x + ((t * dx) % MAP_WIDTH)) % MAP_WIDTH
            currentPositions[p][1] = (y + ((t * dy) % MAP_HEIGHT)) % MAP_HEIGHT

            moveRobot(x, y, currentPositions[p][0], currentPositions[p][1])
        else:
            placeRobot(x, y)

def findXmasTreeWithHeuristic():
    # my heuristic for "most organised" is:
    # 1. Overall distance to centre from all robots is lowest
    lowestDistance = distanceFromCentre()

    # time at which these occur
    distanceTime = 0

    # key insight is that MAP_WIDTH and MAP_HEIGHT are primes, so pattern must repeat after MAP_WIDTH*MAP_HEIGHT cycles
    for time in range(MAP_WIDTH*MAP_HEIGHT):
        for p in range(0, len(currentPositions)):
            x = currentPositions[p][0]
            y = currentPositions[p][1]
            dx = velocities[p][0]
            dy = velocities[p][1]

            currentPositions[p][0] = (x + dx) % MAP_WIDTH
            currentPositions[p][1] = (y + dy) % MAP_HEIGHT

        newDistance = distanceFromCentre()
        if (newDistance < lowestDistance):
            lowestDistance = newDistance
            distanceTime = time 

    return distanceTime+1


# Create an empty map
# ONLY use this for visualisation, not processing
for i in range(MAP_HEIGHT):
    robotMap.append(list(''.ljust(MAP_WIDTH, '.')))

with open("input", "r") as f:
    line = f.readlines()

    for l in line:
        l = l[2:].replace('p=','').replace('v=','').replace('\n', '')
        robot = l.split(' ')
        pos = robot[0].split(',')
        velocity = robot[1].split(',')
        startPoints.append([int(pos[0]), int(pos[1])])
        currentPositions.append([int(pos[0]), int(pos[1])])
        velocities.append([int(velocity[0]), int(velocity[1])])

updatePositionsAtTime(0)

# Got direct to time step 100
updatePositionsAtTime(100)

w = MAP_WIDTH // 2
h = MAP_HEIGHT // 2

for r in robotMap:
   print(''.join(r))

print(f"Robot count: {len(currentPositions)}")
print(f"PART1 Safety factor {calcSafetyFactor()}")

print("PART2")
# Zero the map and get the original start positions
robotMap = []
for i in range(MAP_HEIGHT):
    robotMap.append(list(''.ljust(MAP_WIDTH, '.')))
currentPositions = startPoints.copy()
updatePositionsAtTime(0)

distanceTime = findXmasTreeWithHeuristic()
print(f"PART2 Xmas Tree time at {distanceTime}")
updatePositionsAtTime(distanceTime)
for r in robotMap:
   print(''.join(r))


