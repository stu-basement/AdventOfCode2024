antinodeLocations = set()
areaMap = []

# PART 1
with open("input", "r") as f:
    for line in f.readlines():
        areaMap.append(line)
originalMap = areaMap.copy()
print(originalMap)
print(f"Width {len(areaMap[0]) - 1} Height {len(areaMap)}")

def onMap(x, y):
    return 0 <= x < len(areaMap[0])-1 and 0 <= y < len(areaMap)

def addLocation(x,y,x1,y1,antennaType):
    dx = (x1 - x)
    dy = (y1 - y)

    if onMap(x-dx,y-dy):
        print(f"Add antinode at {x-dx},{y-dy} {dx}-{dy}")
        antinodeLocations.add((x-dx, y-dy))
    if onMap(x1+dx,y1+dy):
        print(f"Add antinode at {x1+dx},{y1+dy} {dx}-{dy}")
        antinodeLocations.add((x1+dx,y1+dy))

for y in range(0, len(areaMap)):
   for x in range(0, len(areaMap[0])-1):
       if (originalMap[y][x] != '.'):
           antennaType = originalMap[y][x]
           print(f"Antenna {antennaType} found at {x},{y}")
           for y1 in range(y, len(areaMap)):
               if (y == y1):
                   startX = x+1
               else:
                   startX = 0
               for x1 in range(startX, len(areaMap[0])-1):
                   if originalMap[y1][x1] == antennaType:
                       # this is an edge
                       print(f"Matching antenna found at {x1},{y1}")
                       addLocation(x,y,x1,y1,antennaType)

locationCount = 0
for l in antinodeLocations:
    ly = l[1]
    lx = l[0]
    areaMap[ly] = areaMap[ly][:lx] + "#" + areaMap[ly][lx+1:]
    locationCount += 1

print(antinodeLocations)

for row in areaMap:
    print(row)

print(f"Locations {locationCount}")

print("PART2")
areaMap = originalMap.copy()
antennaLocations = set()
for y in range(0, len(areaMap)):
    for x in range(0, len(areaMap[0])-1):
        if areaMap[y][x] != '.':
            antennaLocations.add((x,y,areaMap[y][x]))
print(f"Antenna locations: {antennaLocations}")

edges = set()
for id, antenna in enumerate(antennaLocations):
    print(f"Antenna {antenna[2]} at {antenna[0]},{antenna[1]}") 
    for id1, antenna1 in enumerate(antennaLocations):
        if (antenna1[2] == antenna[2]):
            dx = antenna1[0] - antenna[0]
            dy = antenna1[1] - antenna[1]
            if not (dx == 0 and dy == 0):
                edges.add((antenna[0], antenna[1], antenna[2], dx, dy))

print(f"Edges: {edges}")
for e in edges:
    x = e[0]
    y = e[1]
    dx = e[3]
    dy = e[4]

    print(f"Process edge {e}")
    while onMap(x, y):
        print(f"Antinode at {x},{y}")
        antinodeLocations.add((x,y))
        x += dx
        y += dy


locationCount = 0
for l in antinodeLocations:
    ly = l[1]
    lx = l[0]
    areaMap[ly] = areaMap[ly][:lx] + "#" + areaMap[ly][lx+1:]
    locationCount += 1

for row in areaMap:
    print(row)

print(f"Locations {locationCount}")
