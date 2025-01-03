import numpy as np

def onMap(m, x, y):
    return 0 <= x < len(m[0]) and 0 <= y < len(m)

directions = [[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]]
orthogonalDirections = [[0,-1],[1,0],[0,1],[-1,0]]

def validMove(m, x, y, dx, dy, r):
    if onMap(m, x+dx, y+dy):
        cell = m[y+dy][x+dx]
        if (cell == r):
            return True
    return False

def adjacentInRegion(region, x, y, dx, dy, r):
    if (x+dx, y+dy, r) in region:
        return True
    else:
        return False

def regionBoundingBox(region):
    bottomLeftX = min(point[0] for point in region)
    bottomLeftY = min(point[1] for point in region)
    topRightX = max(point[0] for point in region)
    topRightY = max(point[1] for point in region)

    return (bottomLeftX, bottomLeftY), (topRightX, topRightY)

def printRegion(region):
    regionMap = []

    bottomLeft, topRight = regionBoundingBox(region)
    for i in range(abs(topRight[1] - bottomLeft[1]) + 1):
        regionMap.append(list(''.ljust(abs(topRight[0] - bottomLeft[0]) + 1, '.')))

    pointIter = iter(region)
    r = next(pointIter, None)
    while (r != None):
        regionMap[r[1] - bottomLeft[1]][r[0] - bottomLeft[0]] = r[2]
        r = next(pointIter, None)

    return regionMap

def scanRegion(region, m, x, y, r):
    if m[y][x] in '0.':
        return None

    stack = []
    stack.append((x,y,r))
    while len(stack) > 0:
        point = stack.pop()
        if not point in(region) and (point[2] == r):
            region.add(point)

            for d in orthogonalDirections:
                if validMove(m,point[0],point[1],d[0],d[1],r):
                    neighbor = ((point[0]+d[0], point[1]+d[1], r))
                    stack.append(neighbor)

    return region
    
def calcPerimeter(m, region):
    perimeter = 0
    for point in region:
        adjacentCount = 0
        for d in orthogonalDirections:
            if adjacentInRegion(region, point[0], point[1], d[0], d[1], point[2]):
                adjacentCount += 1 

        if (adjacentCount < 0) or (adjacentCount > 4):
            print(f"ERROR at {point[0]},{point[1]} {adjacentCount}")
            for row in regionMap:
                print(f"{''.join(str(c) for c in row)}")

            exit()

        # handle the case where part of a region isn't orthogonally connected
        if (adjacentCount == 0) and (len(region) > 1):
            adjacentCount = 4

        regionMap[point[1]][point[0]] = str(adjacentCount)

        perimeter += (4 - adjacentCount)
    return perimeter

areaMap = []
with open("input", "r") as f:
    for line in f.readlines():
        areaMap.append(list(line.replace('\n','')))

regionMap = areaMap.copy()

print(f"Original map {len(regionMap)} rows of {len(regionMap[0])} columns")
for row in regionMap:
    print(f"{''.join(str(c) for c in row)}")

print("-----")

regions = []
for y in range(0,len(areaMap)):
    for x in range(0, len(areaMap[0])):
        r = areaMap[y][x]

        region = set()
        region = scanRegion(region, regionMap, x, y, r)
        if region != None:
            regions.append(region)
            for p in region:
                regionMap[p[1]][p[0]] = '.'

totalCost = 0
for r in regions:
    area = len(r)
    perimeter = calcPerimeter(regionMap, r)
    totalCost += (area * perimeter)

for row in regionMap:
    print(f"{''.join(str(c) for c in row)}")

print(f"{len(regions)} regions found")

print(f"Total cost {totalCost}")

print("PART2")
# Key insmatrix multiplication 2x2ight for part 2 is that the number of sides is the same as the number of corners
#
# There are eight corner cases
#
# 1 1 and 1 1
# 1 X     X 1 are corners (1 is inside region, X is outside of region)
#
# 1 X     X 1
# 1 1     1 1
#
# X X     X X
# X 1     1 X
#
# X 1     1 X
# X X     X X
insideCorners = { ( 0, 0, 0, 0, 1, 1, 0, 1, 0 ), ( 0, 1, 0, 0, 1, 1, 0, 0, 0 ), ( 0, 1, 0, 1, 1, 0, 0, 0, 0 ), ( 0, 1, 0, 1, 1, 0, 0, 1, 0 ) }
uturns = { ( 0, 0, 0, 1, 1, 0, 0, 0, 0 ), ( 0, 0, 0, 0, 1, 1, 0, 0, 0), ( 0, 1, 0, 0, 1, 0, 0, 0, 0 ), ( 0, 0, 0, 0, 1, 0, 0, 1, 0 ) }
outsideCorners = { ( 0, 0, 0, 0, 1, 1, 0, 1, 0 ), ( 0, 0, 0, 1, 1, 0, 0, 1, 0), (0, 1, 0, 1, 1, 0, 0, 0, 0), ( 0, 1, 0, 0, 1, 1, 0, 0, 0 ) } 
tees = { ( 0, 1, 0, 0, 1, 1, 0, 1, 0 ), ( 0, 0, 0, 1, 1, 1, 0, 1, 0), ( 0, 1, 0, 1, 1, 0, 0, 1, 0 ), ( 0, 1, 0, 1, 1, 1, 0, 0, 0 ) }
singleton = { ( 0, 0, 0, 0, 1, 0, 0, 0, 0) }

regionMap = []
with open("input", "r") as f:
    for line in f.readlines():
        regionMap.append(list(line.replace('\n','')))

for row in regionMap:
    print(f"{''.join(str(c) for c in row)}")

regions = []
for y in range(0,len(regionMap)):
    for x in range(0, len(regionMap[0])):
        r = regionMap[y][x]

        region = set()
        region = scanRegion(region, regionMap, x, y, r)
        if region != None:
            regions.append(region)
            for p in region:
                regionMap[p[1]][p[0]] = '0'

totalPrice = 0
for region in regions:
    calcPerimeter(regionMap, region)
    totalCorners = 0
    pointIter = iter(region)
    p = next(pointIter, None)

    prevCorners = totalCorners
    while p != None:
        # corner detection
        # put feature at centre of 3x3 matrix
#        feature = ( 1 if (p[0]-1, p[1]-1, p[2]) in region else 0, 1 if (p[0],p[1]-1,p[2]) in region else 0, 1 if (p[0]+1,p[1]-1,p[2]) in region else 0,
#                    1 if (p[0]-1, p[1],   p[2]) in region else 0, 1 if (p[0],p[1],  p[2]) in region else 0, 1 if (p[0]+1,p[1],  p[2]) in region else 0,
#                    1 if (p[0]-1, p[1]+1, p[2]) in region else 0, 1 if (p[0],p[1]+1,p[2]) in region else 0, 1 if (p[0]+1,p[1]+1,p[2]) in region else 0 )
        feature = ( 0, 1 if (p[0],p[1]-1,p[2]) in region else 0, 0,
                    1 if (p[0]-1, p[1],   p[2]) in region else 0, 1 if (p[0],p[1],  p[2]) in region else 0, 1 if (p[0]+1,p[1],  p[2]) in region else 0,
                    0, 1 if (p[0],p[1]+1,p[2]) in region else 0, 0 )

        if feature in insideCorners:
            totalCorners += 1
        if feature in uturns:
            totalCorners += 2
        if feature in outsideCorners:
            totalCorners += 1
        if feature in tees:
            totalCorners += 2
        if feature in singleton:
            totalCorners += 4
 
        p = next(pointIter, None)

    if (prevCorners == totalCorners):
        print(f"ERROR: No corners added for this region {region}")

    totalPrice += (len(region) * totalCorners)
      
print(f"Total discounted price {totalPrice}")

for r in regions:
    bottomLeft, topRight = regionBoundingBox(r)
    print(f"Region bounding box {bottomLeft[0]},{bottomLeft[1]} to {topRight[0]},{topRight[1]}")
    regionMap = printRegion(r)
    for r in regionMap:
        print(''.join(r))
