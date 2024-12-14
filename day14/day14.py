robotMap = []
startPoints = []
velocities = []
currentPositions = []

def calcSafetyFactor(w,h):
    quadBR = 0
    quadBL = 0
    quadUL = 0
    quadUR = 0
    for p in currentPositions:
       if (p[1] == h) or (p[0] == w):
           continue

       if (p[1] < h) and (p[0] < w):
           quadUL += 1 

       if (p[1] < h) and (p[0] >= w):
           quadUR += 1

       if (p[1] >= h) and (p[0] >= w):
           quadBR += 1

       if (p[1] >= h) and (p[0] < w):
           quadBL += 1

    return quadUL * quadUR * quadBL * quadBR

def distanceFromCentre():
    totalDistance = 0
    for p in currentPositions:
        totalDistance += abs(p[0] - (MAP_WIDTH //2)) + abs(p[1] - (MAP_HEIGHT // 2))
    return totalDistance

def findMinSafetyFactor():
    lowestDistance = distanceFromCentre()
    xmasTreeTime = 1

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
            xmasTreeTimeDistance = time 

    return (lowestDistance, xmasTreeTimeDistance+1)

MAP_WIDTH = int(101)
MAP_HEIGHT = int(103)

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

print(startPoints)
print(velocities)        

for time in range(100):
    for p in range(0, len(currentPositions)):
        x = currentPositions[p][0]
        y = currentPositions[p][1]
        dx = velocities[p][0]
        dy = velocities[p][1]

        currentPositions[p][0] = (x + dx) % MAP_WIDTH
        currentPositions[p][1] = (y + dy) % MAP_HEIGHT

for c in range (0, len(currentPositions)):
    p = currentPositions[c]
    n = robotMap[p[1]][p[0]]
    
    robotMap[p[1]][p[0]] = str(1 if n =='.' else int(n)+1)

for r in robotMap:
   print(''.join(r))

discardedRobots = 0

w = MAP_WIDTH // 2
h = MAP_HEIGHT // 2

print(f"Quadrants {w} width by {h} height")
for r in robotMap:
   print(''.join(r))


print(f"Robot count: {len(currentPositions)} {discardedRobots} discarded")
print(f"Safety factor {calcSafetyFactor(w, h)}")

print("PART2")
robotMap = []
startPoints = []
velocities = []
currentPositions = []
for i in range(MAP_HEIGHT):
    robotMap.append(list(''.ljust(MAP_WIDTH, '.')))

# make sure we start with clean input
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
print(findMinSafetyFactor())
