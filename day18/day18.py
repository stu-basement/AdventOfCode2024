""" AdventOfCode Day 18 """
from queue import PriorityQueue
from typing import TypeVar

Node = TypeVar("Node")

byte_list = []
obstacles = set()
MEM_WIDTH = 71
MEM_HEIGHT = 71

def heuristic(a, b):
    """ Manhattan distance heuristic for A* search """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def neighbours(node):
    """ Valid neighbours for a square are on the map and not obstacles """
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Left, Right, Up, Down

    return [ (node[0] + nx, node[1] + ny) for nx, ny in directions \
            if 0 <= (node[0] + nx) < MEM_WIDTH and 0 <= (node[1] + ny) < MEM_HEIGHT and \
            (node[0] + nx, node[1] + ny) not in obstacles]

def reconstructPath(prev_nodes, start_node, end_node):
    """ Reconstruct the path from start to end nodes """
    path = set()
    current: Node = end_node
    if end_node not in prev_nodes:
        return []

    while current != start_node and current is not None:
        path.add(current)
        if current is not None:
            current = path_nodes[current]

    return path

def astarSearch(start_node, end_node):
    """ Do an A* search on the memory space from start to end nodes avoiding obstacles """
    frontier = PriorityQueue()

    came_from: dict[Node] = {}
    cost_so_far: dict[Node, int] = {}
    came_from[start_node] = None
    cost_so_far[start_node] = 0

    frontier.put( start_node, 0)
    while not frontier.empty():
        current: Node = frontier.get()

        if current == end_node:
            return came_from, current

        for next_node in neighbours(current):
            new_cost = cost_so_far[current] + 1

            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(next_node, end_node)
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

path_nodes, goal_node = astarSearch( (0,0), (70, 70) )
path = reconstructPath(path_nodes, (0,0), (70,70))
print(f"PART1: {len(path)}")

# Find the next byte that makes the exit unreachable
next_byte = 1025
while goal_node is not None and next_byte < len(byte_list):
    byte = byte_list[next_byte]
    obstacles.add( byte_list[next_byte] )

    if byte in path:
        path_nodes, goal_node = astarSearch( (0,0), (70,70) )

    if goal_node is not None:
        path = reconstructPath(path_nodes, (0,0), (70,70))
        next_byte += 1

if goal_node is None:
    print(f"PART2: First byte to close exit coords {byte_list[next_byte]}")
