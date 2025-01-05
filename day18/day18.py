""" AdventOfCode Day 18 """
from queue import PriorityQueue
from typing import TypeVar

Node = TypeVar("Node")

byte_list = []
obstacles = set()
MEM_WIDTH = 71
MEM_HEIGHT = 71

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def neighbours(node):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Left, Right, Up, Down

    return [ (node[0] + nx, node[1] + ny) for nx, ny in directions \
            if 0 <= (node[0] + nx) < MEM_WIDTH and 0 <= (node[1] + ny) < MEM_HEIGHT and \
            (node[0] + nx, node[1] + ny) not in obstacles]

def reconstructPath(came_from, startNode, endNode):
    path = set()
    current: Node = endNode
    if endNode not in came_from:
        return []

    while current != startNode and current is not None:
        path.add(current)
        if current is not None:
            current = came_from[current]

    return path

def astarSearch(startNode, endNode):
    frontier = PriorityQueue()

    came_from: dict[Node] = {}
    cost_so_far: dict[Node, int] = {}
    came_from[startNode] = None
    cost_so_far[startNode] = 0

    frontier.put( startNode, 0)
    while not frontier.empty():
        current: Node = frontier.get()

        if current == endNode:
             return came_from, current

        for next_node in neighbours(current):
            new_cost = cost_so_far[current] + 1

            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(next_node, endNode)
                frontier.put(next_node, priority)
                came_from[next_node] = current

    return came_from, None

with open("input", "r", encoding="utf-8") as f:
    for line in f.readlines():
        a, b = map(int, line.split(','))
        byte_list.append( (a,b) )

# Get the length of the shortest path after 1024 bytes have fallen
for i in range(1024):
    obstacles.add( byte_list[i] )

came_from, goal_node = astarSearch( (0,0), (70, 70) )
path = reconstructPath(came_from, (0,0), (70,70))
print(f"PART1: {len(path)}")

# Find the next byte that makes the exit unreachable
nextByte = 1025
while goal_node is not None and nextByte < len(byte_list):
    byte = byte_list[nextByte]
    obstacles.add( byte_list[nextByte] )

    if byte in path:
        came_from, goal_node = astarSearch( (0,0), (70,70) )

    if goal_node is not None:
        path = reconstructPath(came_from, (0,0), (70,70))
        nextByte += 1

if goal_node is None:
    print(f"PART2: First byte to close exit coords {byte_list[nextByte]}")
