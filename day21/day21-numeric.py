from queue import PriorityQueue
from typing import TypeVar
from collections import defaultdict

Node = TypeVar("Node")

# Lookup table for the optimal paths between nodes on directional keypads
# Optimal paths: perfer L shape over zigzag
# Prefer < over ^ or v (move left first then up or down)
# Prefer v over > (move down first then right)
# key: (from, to)
# value: move sequence required
directionalLUT = {
        ('A','A'): 'A', ('A','^'): '<A', ('A','<'): 'v<<A', ('A','v'): '<vA', ('A','>'): 'vA',
        ('^','A'): '>A', ('^','>'): 'v>A', ('^', '<'): 'v<A', ('^','v'): 'vA', ('<','A'): '>>^A',
        ('<','^'): '>^A', ('<', 'v'): '>A', ('<', '>'): '>>A', ('v','A'): '^>A',
        ('v','<'): '<A', ('v','>'): '>A', ('v', '^'): '^A',
        ('>','A'): '^A', ('>','^'): '<^A', ('>','v'): '<A', ('>', '<'): '<<A',
        ('^','^'): 'A', ('<','<'): 'A', ('v','v'): 'A', ('>','>'): 'A'}

# There are only 13 valid sequences
sequence_frequencies = {
        ('<A'):  1, ('<vA'): 1, ('v<<A'): 1, ('vA'): 1, ('A'): 1,
        ('v<A'): 1, ('v>A'): 1, ('>^A'): 1, ('^>A'): 1, ('^A'): 1,
        ('>>^A'): 1, ('<^A'): 1, ('>A'): 1}

def numericHeuristic(startNode, direction, endNode):
    addedCost = 0

    if (startNode[0] == '8' and endNode[0] == '4' or \
        (startNode[0] == '9' and endNode[0] == '5') or \
        (startNode[0] == '5' and endNode[0] == '1') or
        (startNode[0] == '6' and endNode[0] == '2')) and direction == 'v':
        addedCost = 1000

    return addedCost

def numericNeighbours(button, direction):
    # Neighbour is a tuple of (button, direction, cost)
    # prefer moving in the same direction
    # prefer left, up, down, right in that order
    n = []

    if button == '0':
        n.append( ('2', '^', 1 if direction in '^v?' else 1000) )
        n.append( ('A', '>', 1 if direction in '<>?' else 1000) )
    elif button == '1':
        n.append( ('4', '^', 1 if direction in '^v?' else 1000) )
        n.append( ('2', '>', 1 if direction in '<>?' else 1000) )
    elif button == '2':
        n.append( ('0', 'v', 1 if direction in '^v?' else 1000) )
        n.append( ('1', '<', 1 if direction in '<>?' else 1000) )
        n.append( ('3', '>', 1 if direction in '<>?' else 1000) )
        n.append( ('5', '^', 1 if direction in '^v?' else 1000) )
    elif button == '3':
        n.append( ('A', 'v', 1 if direction in '^v?' else 1000) )
        n.append( ('2', '<', 1 if direction in '<>?' else 1000) )
        n.append( ('6', '^', 1 if direction in '^v?' else 1000) )
    elif button == '4':
        n.append( ('1', 'v', 1 if direction in 'v^?' else 1000) )
        n.append( ('7', '^', 1 if direction in '^v?' else 1000) )
        n.append( ('5', '>', 1 if direction in '<>?' else 1000) )
    elif button == '5':
        n.append( ('2', 'v', 1 if direction in '^v?' else 1000) )
        n.append( ('4', '<', 1 if direction in '<>?' else 1000) )
        n.append( ('6', '>', 1 if direction in '<>?' else 1000) )
        n.append( ('8', '^', 1 if direction in '^v?' else 1000) )
    elif button == '6':
        n.append( ('5', '<', 1 if direction in '<>?' else 1000) )
        n.append( ('9', '^', 1 if direction in '^v?' else 1000) )
        n.append( ('3', 'v', 1 if direction in 'v^?' else 1000) )
    elif button == '7':
        n.append( ('4', 'v', 1 if direction in 'v^?' else 1000) )
        n.append( ('8', '>', 1 if direction in '<>?' else 1000) )
    elif button == '8':
        n.append( ('7', '<', 1 if direction in '<>?' else 1000) )
        n.append( ('5', 'v', 1 if direction in '^v?' else 1000) )
        n.append( ('9', '>', 1 if direction in '<>?' else 1000) )
    elif button == '9':
        n.append( ('8', '<', 1 if direction in '<>?' else 1000) )
        n.append( ('6', 'v', 1 if direction in '^v?' else 1000) )
    elif button == 'A':
        n.append( ('0', '<', 1 if direction in '<>?' else 1000) )
        n.append( ('3', '^', 1 if direction in '^v?' else 1000) )

    return n

def reconstructPath(visited, sn, en):
    """ Return the string for the path between two digits """
    p = []
    current: Node = en

    while current != sn and current is not None:
        p.append(current[1])
        if current is not None:
            current = visited[current]
    p.reverse()

    return ''.join(p) + 'A'

def astarSearch(sn, en, neighbours, heuristic):
    """ Search for the best path between digits on the numeric pad """
    frontier = PriorityQueue()

    came_from: dict[Node] = {}
    cost_so_far: dict[Node, int] = {}
    came_from[sn] = None
    cost_so_far[ sn ] = 0
    bestCost = None
    goalNode = None

    frontier.put( sn, 0)
    while not frontier.empty():
        current: Node = frontier.get()
        if current[0] == en[0]:
            if bestCost is None or cost_so_far[current] < bestCost:
                bestCost = cost_so_far[current]
                goalNode = current
            continue

        for n in neighbours(current[0], current[1]):
            new_cost = cost_so_far[ current ] + n[2]

            if n not in cost_so_far or new_cost < cost_so_far[n]:
                cost_so_far[ n ] = new_cost + heuristic(current, n[1], endNode)
                priority = new_cost
                frontier.put(n, priority)
                came_from[n] = current

    return came_from, goalNode

def initialPath(seq_freq, sequences):
    """ Return the path complexity of a list of sequences """
    # this will be the path length at this level
    # frequency of sequences generated by this robot
    # key: sequence, value = frequency
    robot_sequences = defaultdict()

    for sequence in sequences:
        startAt = 'A'
        for move in sequence:
            sequence_generated = directionalLUT[startAt, move]
            if sequence_generated not in robot_sequences:
                robot_sequences[sequence_generated] = seq_freq[sequence_generated]
            else:
                robot_sequences[sequence_generated] += seq_freq[sequence_generated]
            startAt = move

    return robot_sequences

codes = []
with open("input", "r", encoding="utf-8") as f:
    line = f.readline()
    while len(line):
        codes.append(line.replace('\n', ''))
        line = f.readline()

startNodeNumeric = ('A', '?', 0)
total_complexity = 0
for c in codes:
    numericPresses = []
    paths = []
    # Find the sequence of button presses for the numeric keypad
    for button in c:
        endNode = (button, 0)

        path_nodes, goal_state = \
                astarSearch(startNodeNumeric, endNode, numericNeighbours, numericHeuristic)
        paths.append( reconstructPath(path_nodes, startNodeNumeric, goal_state) )
        startNodeNumeric = (goal_state[0], '?', 0)

    # generate the base sequence frequencies
    level_frequencies = initialPath(sequence_frequencies, paths)

    # now multiply these frequencies by the frequency
    # of each sequence generated by each robot
    for level in range(24):
        robot_sequences = {}
        for k, v in level_frequencies.items():
            startAt = 'A'
            for move in k:
                sequence_generated = directionalLUT[startAt, move]
                if sequence_generated not in robot_sequences:
                    robot_sequences[sequence_generated] = level_frequencies[k]
                else:
                    robot_sequences[sequence_generated] += level_frequencies[k]
                startAt = move

        level_frequencies = robot_sequences
    code_complexity = sum( len(k) * v for k, v in robot_sequences.items() )
    total_complexity += (int(c[:3]) * code_complexity)

print(f"PART2: Total complexity {total_complexity}")
