def onMap(x, y):
    return 0 <= x < len(areaMap[0]) and 0 <= y < len(areaMap)


# up, right, down, left
directions = [[0, -1], [1, 0], [0,1], [-1,0]] 
edges = set()

# PART 1
areaMap = []
with open("input", "r") as f:
    for line in f.read().splitlines():
        areaMap.append(list(line))

for line in areaMap:
    print(f"{line}")

print(f"Width {len(areaMap)} x height {len(areaMap)}")
for y in range(0, len(areaMap)):
    for x in range (0, len(areaMap[0])):
        for d in directions:
            nextX = x + d[0]
            nextY = y + d[1]
            if onMap(nextX, nextY):
                # if this step would be in an orthogonal direction up one step, add an edge between nodes
                if int(areaMap[nextY][nextX]) == int(areaMap[y][x]) + 1:
                    edges.add((x, y, nextX, nextY)) 

for e in edges:
    print(f"Edge: {e[0]}, {e[1]} to {e[2]},{e[3]}")

trailheads = set()
trails = []
# Make a set of starting locations (starting at 0)
for y in range(0, len(areaMap)):
    for x in range(0,len(areaMap[0])):
        if (int(areaMap[y][x]) == 0):
            trailheads.add((x, y))

print(f"Trailheads {trailheads}") 

tops = set()
for t in trailheads:
    print(f"Walk trailhead starting at {t[0]},{t[1]}")
    startX = t[0]
    startY = t[1]

    s = list()
    v = (startX, startY, False)
    s.append([v, [[startX, startY]]])
    while len(s) > 0:
        (v,path) = s.pop()
        if not v[2]:
            print(f"Node {v[0]},{v[1]} not visited")
            if (int(areaMap[v[1]][v[0]]) == 9):
                print(f"Top of trail found at {v[0]},{v[1]} {path}")
                print(f"Path {path}")
                tops.add((t[0], t[1], v[0],v[1]))
                trails.append(path)

            v = (v[0], v[1], True)
            print(f"Visit {v[0]},{v[1]}")
            for e in edges:
                if (e[0] == v[0]) and (e[1] == v[1]):
                    print(f"Add to stack neighbour {e[2]},{e[3]} and path so far {path}")
                    p = path.copy()
                    p.append([e[2], e[3]])
                    s.append([(e[2], e[3], False), p])
 
totalScore = 0
for t in trailheads:
    for tr in tops:
        if (t[0] == tr[0]) and (t[1] == tr[1]):
            totalScore += 1
 
print(f"Trailhead score {totalScore}")

print(f"Number of trails {len(trails)}")
ratingScore = 0
for t in trailheads:
    for tr in trails:
        if (t[0] == tr[0][0]) and (t[1] == tr[0][1]):
            ratingScore += 1

print(f"Trailhead rating {ratingScore}")
