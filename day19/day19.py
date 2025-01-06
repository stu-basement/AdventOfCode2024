""" AdventOfCode Day19 """

towels = set()
designs = []

def neighbours(current, towel_patterns):
    """ Neighbours of the current towel are the patterns that it starts with """
    n = []

    if current not in towel_patterns:
        for p in towel_patterns:
            splits = current.partition(p)
            if splits[0] == '' and splits[2]:
                n.append( splits[2] )

    return n

def searchTowels(design, towel_patterns):
    """ Search the design for possible towel compostions """
    visited = []
    s = []

    s.append( design )
    while s:
        current = s.pop()

        # Goal state: design has been reduced to a collection
        # where each element is in the set of towels
        if current in towel_patterns:
            return True

        if current not in visited:
            visited.append( current )
            next_towels = neighbours(current, towel_patterns)
            for n in next_towels:
                s.append(n)

    return False

def countTowels(design, towel_patterns):
    """ Count the possible ways of making a design from the set of towels """
    designTowels = {"": 1}

    while designTowels:
        towel, count = sorted(designTowels.items(), key=lambda x: len(x[0]))[0]
        if towel == design:
            return count

        fragment = [ towel + t for t in towel_patterns if design[len(towel):].startswith(t) ]
        for fr in fragment:
            designTowels[fr] = designTowels[fr] + count if fr in designTowels else count

        del designTowels[towel]

    return 0

with open("input", "r", encoding="utf-8") as f:
    line = f.readline().replace('\n', '')
    while line:
        for t in line.strip().split(', '):
            towels.add( (t) )
        line = f.readline().replace('\n', '')

    line = f.readline().replace('\n', '')
    while line:
        designs.append(line.strip())
        line = f.readline().replace('\n', '')

valid_designs = sum( searchTowels(design, towels) for design in designs )
print(f"PART1: Valid designs {valid_designs}")

total_combos = sum( countTowels(design, towels) for design in designs )
print(f"PART2 (dictionary) {total_combos}")
