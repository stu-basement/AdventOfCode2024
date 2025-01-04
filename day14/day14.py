""" AdventOfCode Day 14 """
from operator import mul
from functools import reduce

MAP_WIDTH = int(101)
MAP_HEIGHT = int(103)

robotMap = []
robots = []

def findXmasTree():
    """ Find the hidden Xmas tree pattern """
# my heuristic for "most organised" is: Overall distance to centre from all robots is lowest
    lowest_distance = ( sum( (abs(x - (MAP_WIDTH // 2)) + abs(y - (MAP_HEIGHT // 2))) \
                for x, y, _, _ in robots), 0 )

    # key insight is that MAP_WIDTH and MAP_HEIGHT are primes,
    # so pattern must repeat after MAP_WIDTH*MAP_HEIGHT cycles
    for t in range(MAP_WIDTH * MAP_HEIGHT):
        for n, (x, y, dx, dy) in enumerate(robots):
            robots[n] = ( (x + dx) % MAP_WIDTH, (y + dy) % MAP_HEIGHT, dx, dy )

        distance = sum((abs(x - MAP_WIDTH // 2) + abs(y - MAP_HEIGHT // 2)) \
                for x, y, _, _ in robots)

        if distance < lowest_distance[0]:
            lowest_distance = ( distance, t + 1 )

    return lowest_distance[1]

with open("input", "r", encoding="utf-8") as f:
    line = f.readlines()

    for l in line:
        l = l[2:].replace('p=','').replace('v=','').replace('\n', '')
        robot = l.split(' ')
        pos = robot[0].split(',')
        velocity = robot[1].split(',')
        robots.append( (int(pos[0]), int(pos[1]), int(velocity[0]), int(velocity[1])))
    start_robots = robots.copy()

# Part 1 - Go direct to time step 100
for n, (x, y, dx, dy) in enumerate(robots):
    robots[n] = ( (x + (100 * dx) % MAP_WIDTH) % MAP_WIDTH, \
            (y + (100 * dy) % MAP_HEIGHT) % MAP_HEIGHT, dx, dy )

quadrants = [ [-1, -1], [1, -1], [-1, 1], [1, 1] ]
print("PART1 Safety Factor: ", \
        reduce(mul, (sum( (x - MAP_WIDTH // 2) * q[0] > 0 and (y - MAP_HEIGHT // 2) * q[1] > 0 \
            for x, y, _, _ in robots) for n, q in enumerate(quadrants))))

# Zero the map and get the original start positions
robotMap = []
for i in range(MAP_HEIGHT):
    robotMap.append(list(''.ljust(MAP_WIDTH, '.')))
robots = start_robots.copy()

distanceTime = findXmasTree()
print(f"PART2 Xmas Tree time at {distanceTime}")
for n, (x, y, dx, dy) in enumerate(robots):
    robots[n] = ( (x + (distanceTime * dx) % MAP_WIDTH) % MAP_WIDTH, \
            (y + (distanceTime * dy) % MAP_HEIGHT) % MAP_HEIGHT, dx, dy )
for x, y, _, _ in robots:
    n = robotMap[y][x]
    if n == '.':
        robotMap[y][x] = str(1)
    else:
        robotMap[y][x] = str(int(n)+1)

for r in robotMap:
    print(''.join(r))
