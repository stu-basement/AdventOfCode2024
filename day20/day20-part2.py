from queue import PriorityQueue
from collections import defaultdict
from typing import TypeVar

Node = TypeVar("Node")

def withinTwo(m, p, tp):
    dx = tp[0] - p[0]
    dy = tp[1] - p[1]

    x = p[0]
    y = p[1]
    if (abs(dx) == 2 and abs(dy) == 0) or (abs(dy) == 2 and abs(dx) == 0):
        if (dx == 0):
            wallY = y + (dy // 2)
#            print(f"Points {p},{tp} within two {dx},{dy}, check for wall at {x},{wallY}")
            wallBetween = m[wallY][x] in '#'
        else:
            wallX = x + (dx // 2)
#            print(f"Points {p},{tp} within two {dx},{dy}, check for wall at {wallX},{y}")
            wallBetween = m[y][wallX] in '#'

        return wallBetween        

    return False

def heuristic(a, b):
    distance = abs(a[0] - b[0]) + abs(a[1] - b[1])
    return distance
    return 0

def neighboursNoCollision(m, x, y, dx, dy):
    n = []
    n.append( (x+1, y, 1, 0, 1) )
    n.append( (x-1, y, -1, 0, 1) )
    n.append( (x, y+1, 0, 1, 1) )
    n.append( (x, y-1, 0, -1, 1) )

    return n

def neighbours(m, x, y, dx, dy):
    # Neighbour is a tuple of (x, y, dx, dy, cost)
    n = []

    if m[y][x+1] not in '#':
        n.append( (x+1, y, 1, 0, 1) )
    if m[y][x-1] not in "#":
        n.append( (x-1, y, -1, 0, 1) )

    if m[y-1][x] not in '#':
        n.append( (x, y-1, 0, -1, 1) )

    if m[y+1][x] not in '#':
        n.append( (x, y+1, 0, 1, 1) )

    return n

def reconstructPath(came_from, startNode, endNode):
    path = []
    current: Node = endNode
    if (endNode) not in came_from:
        print("ERROR: No path found")
        return []

    while current != startNode and current != None:
        path.append(current)
        if (current != None):
            current = came_from[current]

    path.reverse()

    return path

def constructPathSet(came_from, startNode, endNode):
    pathPoints = set()

    path = reconstructPath(came_from, startNode, endNode)

    for p in range(0, len(path)):
        pathPoints.add( ( (path[p][0], path[p][1] ), p) )

    print(f"Path points as a set")
    return pathPoints
    

def astarSearch(m, startNode, endNode, neighbourFunc):
    frontier = PriorityQueue()
    n = (startNode[0], startNode[1], 1, 0, 0)

    came_from: dict[Node] = {}
    cost_so_far: dict[Node, int] = {}
    came_from[n] = None
    cost_so_far[n] = 0
    bestCost = None
    goalNode = None

    frontier.put( n, 0)
    while not frontier.empty():
        current: Node = frontier.get()

        if (current[0] == endNode[0] and current[1] == endNode[1]):
            print(f"Goal found with {current}")
            if bestCost == None:
                bestCost = cost_so_far[current]
                goalNode = current
            if cost_so_far[current] < bestCost:
                bestCost = cost_so_far[current]
                goalNode = current
            continue

        if bestCost != None and cost_so_far[current] >= bestCost:
            continue

        for next in neighbourFunc(m, current[0], current[1], current[2], current[3]):
            new_cost = cost_so_far[current] + next[4]

            if next not in cost_so_far:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, endNode)
                frontier.put(next, priority)
                came_from[next] = current
            else:
                if new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(next, endNode)
                    frontier.put(next, priority)
                    came_from[next] = current
                elif new_cost == cost_so_far[next]:
                    came_from[next] = current
                
    return came_from, cost_so_far, goalNode

mazeMap = []

with open("input", "r") as f:
    line = f.readline()
    while (len(line) > 1):
        mazeMap.append(list(line.replace('\n', '')))
        line = f.readline()

for m in range(0, len(mazeMap)):
    for n in range(0, len(mazeMap[0])):
        if mazeMap[m][n] == 'E':
            endNode = (n, m, None, None, None)
        if mazeMap[m][n] == 'S':
            startNode = (n, m, None, None, None)

for r in mazeMap:
    print(''.join(r))
print(f"Start: {startNode}")
print(f"End: {endNode}")

came_from, cost_so_far, goal_state = astarSearch(mazeMap, startNode, endNode, neighbours)
if goal_state != None:
    print(goal_state)
    path = reconstructPath(came_from, startNode, goal_state)
else:
    print("No goal found")
    exit()

steps = 0
turns = 0
if len(path) > 0:
    dx = 1
    dy = 0
    s = path[0]
    for n in range(1, len(path)):
        if (s[0]+dx == path[n][0] and s[1]+dy == path[n][1]):
            steps += 1
        else:
            dx = path[n][0] - s[0]
            dy = path[n][1] - s[1]
            turns += 1

        if (dx == 1):
            stepChar=">"
        elif (dx == -1):
            stepChar="<"
        elif (dy == 1):
            stepChar="v"
        elif (dy == -1):
            stepChar="^"
        else:
            stepChar='X'

        mazeMap[s[1]][s[0]] = stepChar
        s = path[n]

for r in mazeMap:
    print(''.join(r))

points = constructPathSet(came_from, startNode, goal_state)
print(f"Number of points: {len(points)}")
print(points)

savings = []
#for p in points:
#    for q in points:
#        if p[0] != q[0]:
#            if withinTwo(mazeMap, p[0], q[0]):
#                savings.append( (p, q, abs(q[1] - p[1]) - 2) )

for p in points:
    for q in points:
        pathDistance = abs(q[1] - p[1])
        manhattanDistance = abs(q[0][0] - p[0][0]) + abs(q[0][1] - p[0][1])
        if p != q and pathDistance >= 100 and manhattanDistance <= 20:
            print(f"Points {p} and {q} save {pathDistance} for a shortcut of {pathDistance - manhattanDistance}")
            savings.append( (p, q, pathDistance - manhattanDistance) )

savings.sort(reverse=True, key=lambda x: x[2])
groupSavings = dict()
savingsOver100 = 0
for s in savings:
    if ( s[2] ) not in groupSavings:
        groupSavings[s[2]] = 1
    else:
        count = groupSavings[s[2]]
        groupSavings[s[2]] = count+1

for k, v in groupSavings.items():
    print(f"{v // 2} cheats save {k} picoseconds")
    if (k >= 100):
        savingsOver100 += (v//2)
print(f"{savingsOver100} cheats save at least 100 picoseconds")

