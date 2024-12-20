from queue import PriorityQueue
from collections import defaultdict
from typing import TypeVar

Node = TypeVar("Node")

def heuristic(a, b):
    distance = abs(a[0] - b[0]) + abs(a[1] - b[1])
    return distance
    return 0

def neighbours(m, x, y, dx, dy):
    # Neighbour is a tuple of (x, y, dx, dy, cost)
    n = []

    print(f"Neighbours for {x},{y} heading {dx},{dy}")
    # don't return backwards neighbour
    if (dy == 1 or dy == -1):
        if m[y][x-1] not in '#':
            n.append( (x-1, y, -1, 0, 1000) )
        if m[y+dy][x] not in '#':
            n.append( (x, y+dy, 0, dy, 1) )
        if m[y][x+1] not in '#':
            n.append( (x+1, y, 1, 0, 1000) )

    if (dx == 1 or dx == -1):
        if m[y-1][x] not in '#':
            n.append( (x, y-1, 0, -1, 1000 ) )
        if m[y][x+dx] not in '#':
            n.append( (x+dx, y, dx, 0, 1) )
        if m[y+1][x] not in '#':
            n.append( (x, y+1, 0, 1, 1000) )

    print(f"Neighbours for {x},{y} heading {dx},{dy}: {n}")
    return n

def reconstructPath(came_from, startNode, endNode):
    path = []
    current: Node = endNode
    if (endNode) not in came_from:
        print("ERROR: No path found")
        return []

    while current != startNode and current != None:
        path.append(current)
        print(f"Reconstructing path from {current}")
        if (current != None):
            current = came_from[current]

    path.reverse()

    return path

def astarSearch(m, startNode, endNode):
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
            print(f"Cost to reach here {cost_so_far[current]} best so far {bestCost}")
            continue

        if bestCost != None and cost_so_far[current] >= bestCost:
            continue

        for next in neighbours(m, current[0], current[1], current[2], current[3]):
            print(f"Add neighbour {next} from {current} with {current[2]},{current[3]}")
            new_cost = cost_so_far[current] + next[4]
            if (current[2] == next[2]) and (current[3] == next[3]):
                print("Step")
            else:
                print(f"Turn to {next[2]},{next[3]}")

            if next not in cost_so_far:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, endNode)
                print(f"Put {next} with priority {priority}")
                frontier.put(next, priority)
                came_from[next] = current
            else:
                if new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(next, endNode)
                    print(f"Put {next} with priority {priority}")
                    frontier.put(next, priority)
                    came_from[next] = current
                elif new_cost == cost_so_far[next]:
                    print(f"Add equally good option {current} with cost {new_cost}")
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

came_from, cost_so_far, goal_state = astarSearch(mazeMap, startNode, endNode)
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
            print(f"To get to {s[0]},{s[1]} step {dx},{dy}")
            steps += 1
        else:
            dx = path[n][0] - s[0]
            dy = path[n][1] - s[1]
            print(f"At {s[0]},{s[1]} turn to {dx},{dy}")
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
print(f"{steps} steps {turns} turns total {len(path) - 1 + (1000* turns)}")
