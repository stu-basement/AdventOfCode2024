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

# Calculate the possible moves - each valid move is an edge between grid locations
for y in range(0, len(areaMap)):
    for x in range (0, len(areaMap[0])):
        for d in directions:
            nextX = x + d[0]
            nextY = y + d[1]
            if onMap(nextX, nextY):
                # if this step would be in an orthogonal direction up one step, add an edge between nodes
                if int(areaMap[nextY][nextX]) == int(areaMap[y][x]) + 1:
                    edges.add((x, y, nextX, nextY)) 

# Make the set of trailhead locations - each grid cell with 0 is a trailhead
trailheads = set()
trails = []
# Make a set of starting locations (starting at 0)
for y in range(0, len(areaMap)):
    for x in range(0,len(areaMap[0])):
        if (int(areaMap[y][x]) == 0):
            trailheads.add((x, y))

# Calculate the paths from trailheads to tops
tops = set()
for t in trailheads:
    startX = t[0]
    startY = t[1]

    # DFS through the edges from each starting point
    s = list()
    v = (startX, startY, False)
    s.append([v, [[startX, startY]]])
    while len(s) > 0:
        (v,path) = s.pop()
        if not v[2]:
            if (int(areaMap[v[1]][v[0]]) == 9):
                # full path from trailhead to top found
                tops.add((t[0], t[1], v[0],v[1]))
                trails.append(path)

            v = (v[0], v[1], True)
            for e in edges:
                if (e[0] == v[0]) and (e[1] == v[1]):
                    p = path.copy()
                    p.append([e[2], e[3]])
                    s.append([(e[2], e[3], False), p])

# Part 1 answer is the total number of tops reachable from all trailheads 
totalScore = 0
for t in trailheads:
    for tr in tops:
        if (t[0] == tr[0]) and (t[1] == tr[1]):
            totalScore += 1
 
print(f"PART1 Trailhead score {totalScore}")

# Part 2 answer is the total number of paths to all tops from all trailheads
ratingScore = 0
for t in trailheads:
    for tr in trails:
        if (t[0] == tr[0][0]) and (t[1] == tr[0][1]):
            ratingScore += 1

print(f"PART2 Trailhead rating {ratingScore}")
