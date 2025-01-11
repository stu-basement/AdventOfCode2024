from collections import defaultdict

# Lookup table for the optimal paths between nodes on directional keypads
# Optimal paths: perfer L shape over zigzag
# Prefer < over ^ or v (move left first then up or down)
# Prefer v over > (move down first then right)
# key: (from, to)
# value: move string
directionalLUT = {
        ('A','A'): 'A', ('A','^'): '<A', ('A','<'): 'v<<A', ('A','v'): '<vA', ('A','>'): 'vA', \
        ('^','A'): '>A', ('^','>'): 'v>A', ('^', '<'): 'v<A', ('^','v'): 'vA', \
        ('<','A'): '>>^A', ('<','^'): '>^A', ('<', 'v'): '>A', ('<', '>'): '>>A', \
        ('v','A'): '^>A', ('v','<'): '<A', ('v','>'): '>A', ('v', '^'): '^A', \
        ('>','A'): '^A', ('>','^'): '<^A', ('>','v'): '<A', ('>', '<'): '<<A', \
        ('^','^'): 'A', ('<','<'): 'A', ('v','v'): 'A', ('>','>'): 'A'}

#codes = ['029A','980A','179A','456A','379A']
#paths = ['<A^A>^^AvvvA', '^^^A<AvvvA','^<<A^^A>>A', '^^<<A>A>AvvA', '^A^^<<A>>AvvvA']
#codes = ['029A']
#paths = ['<A', '^A', '>^^A', 'vvvA']
codes = ['980A']
paths = ['^^^A', '<A', 'vvvA', ">A"]
#codes = ['456A']
#paths = ['^^<<A', '>A', '>A', 'vvA']

path_complexity = 0
for n, c in enumerate(codes):
    robot_sequences = defaultdict()
    stack = []

    for p in paths:
        stack.append( (0, p) )

    while stack:
        level, path = stack.pop()

        # this is the top level - look up the cost of each move
        startAt = 'A'
        for m in path:
            this_seq = directionalLUT[startAt, m]

            # cost at this level is the length of the path plus the cost of
            # each chunk at the next level up
            # stack this sequence up to the top level
            if (level < 16):
                stack.append( (level + 1, this_seq) )
            else:
                if m not in robot_sequences:
                    robot_sequences[m] = 1
                else:
                    robot_sequences[m] += 1
            startAt = m

    path_length = sum( v * len(k) for k, v in robot_sequences.items() )
    print(f"Code {c} sequence length {path_length}")
    path_complexity += int(c[:3]) * path_length
    print(f"Code {c} complexity {int(c[:3]) * path_length}")
print(f"Total complexity {path_complexity}")
