""" AdventOfCode Day 20 """
from queue import PriorityQueue
from typing import TypeVar

Node = TypeVar("Node")

walls = set()

def heuristic(a, b):
    """ USe ManhattanDistance as heuristic for A* search """
    distance = abs(a[0] - b[0]) + abs(a[1] - b[1])
    return distance

def neighbours(w, x, y, dx, dy):
    """ Return neighbours of a location in up/down/left/right directions that are not in walls """
    dirs = [ [0, -1], [1, 0], [0, 1], [-1, 0] ]
    return [ (x+dx, y+dy, dx, dy, 1) for dx, dy in dirs if (x+dx, y+dy) not in w ]

def reconstructPath(came_from, sp, ep):
    """ Reconstruct the path through individual squares from start to end """
    path = []
    current: Node = ep
    if ep not in came_from:
        print("ERROR: No path found")
        return []

    while current != sp and current is not None:
        path.append(current)
        if current is not None:
            current = came_from[current]

    path.reverse()

    return path

def constructPathSet(came_from, s, e):
    """ Construct the path as a dictionary (x, y): step) """
    pathPoints = {}

    path = reconstructPath(came_from, s, e)

    for n, p in enumerate(path):
        pathPoints[(p[0], p[1])] =  n

    return pathPoints

def astarSearch(w, sn, en):
    """ A* search from start to end given walls """
    frontier = PriorityQueue()
    n = (sn[0], sn[1], 1, 0, 0)

    came_from: dict[Node] = {}
    cost_so_far: dict[Node, int] = {}
    came_from[n] = None
    cost_so_far[n] = 0
    bestCost = None
    goalNode = None

    frontier.put( n, 0)
    while not frontier.empty():
        current: Node = frontier.get()

        if (current[0] == en[0] and current[1] == en[1]):
            if bestCost is None or cost_so_far[current] < bestCost:
                bestCost = cost_so_far[current]
                goalNode = current
            continue

        if bestCost is not None and cost_so_far[current] >= bestCost:
            continue

        for next_node in neighbours(w, current[0], current[1], current[2], current[3]):
            new_cost = cost_so_far[current] + next_node[4]

            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(next_node, endNode)
                frontier.put(next_node, priority)
                came_from[next_node] = current
            elif new_cost == cost_so_far[next_node]:
                came_from[next_node] = current

    return came_from, goalNode

map_height = 0
startNode = endNode = None
with open("input", "r", encoding="utf-8") as f:
    line = f.readline().replace('\n', '')
    while len(line) > 1:
        for x, square in enumerate(list(line)):
            if square == '#':
                walls.add( (x, map_height) )
            elif square == 'E':
                endNode = (x, map_height, None, None, None)
            elif square == 'S':
                startNode = (x, map_height, None, None, None)
        line = f.readline()
        map_height += 1

path_nodes, goal_state = astarSearch(walls, startNode, endNode)
points = constructPathSet(path_nodes, startNode, goal_state)

directions = [ [0, -2], [2, 0], [0, 2], [-2, 0], \
        [1, -1], [1, 1], [-1, 1], [-1, -1], \
        [0, -1], [1, 0], [0, 1], [-1, 0] ]

savings = [ v - points[(k[0]+dx, k[1]+dy)] - 2 for k, v in points.items() \
        for dx, dy in directions \
        if ( k[0] + dx, k[1] + dy ) in points ]

savings.sort(reverse=True)
groupSavings = {}
savingsOver100 = 0
for saving in savings:
    if ( saving ) not in groupSavings:
        groupSavings[saving] = 1
    else:
        groupSavings[saving] = groupSavings[saving]+1

savingsOver100 = sum( v for k, v in groupSavings.items() if k >= 100)
print(f"PART1: {savingsOver100} cheats save at least 100 picoseconds")

# look for points within the Manhattan distance of 20 that would save more than 100
directions = [ (x, y) for x in range(-20, 21) for y in range(-20, 21) if abs(x) + abs(y) <= 20 ]
savings = [ v - points[ (k[0]+dx, k[1]+dy) ]  - abs(dx) - abs(dy) \
        for k, v in points.items() for dx, dy in directions \
        if (k[0] + dx, k[1] + dy) in points and \
        abs(dx) + abs(dy) <= 20 and k != (k[0]+dx,k[1]+dy) and \
        abs(v - points[ (k[0]+dx, k[1]+dy )]) >= 100 ]
savings.sort(reverse=True)
groupSavings = {}
savingsOver100 = 0
for saving in savings:
    if ( saving ) not in groupSavings:
        groupSavings[saving] = 1
    else:
        groupSavings[saving] = groupSavings[saving]+1

savingsOver100 = sum( v for k, v in groupSavings.items() if k >= 100)
print(f"PART2: {savingsOver100} cheats save at least 100 picoseconds")
