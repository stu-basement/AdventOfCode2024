""" AdventOfCode Day 16 """
from queue import PriorityQueue
from typing import TypeVar

Node = TypeVar("Node")

def heuristic(a, b):
    """ Manhattan distance is the heuristic for A* """
    distance = abs(a[0] - b[0]) + abs(a[1] - b[1])
    return distance

def neighbours(w, x, y, dx, dy):
    """ Return the neighbours of a square - valid setsp or turns """
    # Neighbour is a tuple of (x, y, dx, dy, cost)
    n = []

    # don't return backwards neighbour
    # ust a T-shape centred on (x, y)
    if dy != 0:
        if (x - 1, y) not in w:
            n.append( (x-1, y, -1, 0, 1001) )
        if (x, y + dy) not in w:
            n.append( (x, y+dy, 0, dy, 1) )
        if (x + 1, y) not in w:
            n.append( (x+1, y, 1, 0, 1001) )

    if dx != 0:
        if (x, y - 1) not in w:
            n.append( (x, y-1, 0, -1, 1001 ) )
        if (x + dx, y) not in w:
            n.append( (x+dx, y, dx, 0, 1) )
        if (x, y + 1) not in w:
            n.append( (x, y+1, 0, 1, 1001) )

    return n

def astarSearch(w, sn, en):
    """ Perform an A* search on the map from start to end node """

    # Return all possible best paths
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

    return came_from, bestCost, goalNode

map_height = 0
startNode = endNode = None
walls = set()

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

came_from, best_cost, goal_state = astarSearch(walls, startNode, endNode)

print(f"PART1: {best_cost}")
