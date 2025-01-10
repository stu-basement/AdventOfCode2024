""" AdventOfCode Day 12 """
from scipy.signal import convolve2d
import numpy as np

def onMap(m, x, y):
    """ Check that a square is on the map """
    return 0 <= x < len(m[0]) and 0 <= y < len(m)

orthogonalDirections = [[0,-1],[1,0],[0,1],[-1,0]]
regionMap = []

def validMove(m, rx, ry, dx, dy, r_id):
    """ Check that the square in dx, dy direction is still part of this region """
    return onMap(m, rx+dx, ry+dy) and m[ry+dy][rx+dx] == r_id

def regionBoundingBox(r):
    """ Calculate the rectangular bounding box for a region """
    bottomLeftX = min(point[0] for point in r)
    bottomLeftY = min(point[1] for point in r)
    topRightX = max(point[0] for point in r)
    topRightY = max(point[1] for point in r)

    return (bottomLeftX, bottomLeftY), (topRightX, topRightY)

def scanRegion(r, m, startX, startY, r_id):
    """ Scan all of the connected points for a region """
    stack = []
    stack.append( (startX,startY,r_id) )
    while stack:
        point = stack.pop()
        if point not in r and (point[2] == r_id):
            r.add(point)

            for dx, dy in orthogonalDirections:
                if validMove(m,point[0],point[1],dx,dy,r_id):
                    neighbor = ((point[0]+dx, point[1]+dy, r_id))
                    stack.append(neighbor)

    return region

with open("input", "r", encoding="utf-8") as f:
    for line in f.readlines():
        regionMap.append(list(line.replace('\n','')))

map_width = len(regionMap[0])
map_height = len(regionMap)

# isolate each region and remove from the map as we go
regions = []
for y in range(map_height):
    for x in range(map_width):
        # each region is a set of (x, y, r) where x, y is each point
        # contained in the region identified by letter in r
        if regionMap[y][x] not in '0.':
            region = set()
            region = scanRegion(region, regionMap, x, y, regionMap[y][x])
            regions.append(region)
            for p in region:
                regionMap[p[1]][p[0]] = '.'

totalCost = sum( len(r) * sum( 4 - sum( (px + dx, py + dy, pr) in r \
            for dx, dy in orthogonalDirections ) \
            for px, py, pr in r ) for r in regions )
print(f"{len(regions)} regions found")

print(f"PART1: Total cost {totalCost}")

print("PART2")
# Kernel for detecting corners i [-1, 1], [1, -1]
# For each region, make a 0/1 map of the points it contains
# Convolve the kernel over the pa to count the corners per region

totalPrice = 0
corner_kernel = [ [-1,1], [1, -1] ]
for region in regions:
    # start with a blank map sized to the region
    (blX, blY), (trX, trY) = regionBoundingBox(region)
    region_points = np.zeros( (abs(trX - blX) + 1, abs(trY - blY) + 1) )

    # fill 1s for every point in the region
    for x,y,_ in region:
        region_points[abs(x - blX)][abs(y - blY)] = 1

    # convolve with the corner-detection kernel to yield +/-1 at each corner
    result = convolve2d(region_points, corner_kernel)
    totalPrice += int(len(region) * np.sum(np.abs(result)))

print(f"PART2: Total discounted price {totalPrice}")
