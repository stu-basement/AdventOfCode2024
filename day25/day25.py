""" AdventOfCode Day 25 """
keys = []
locks = []

with open("input", "r", encoding="utf-8") as f:
    line = f.readline()
    while len(line) > 1:
        if line[0] == '#':
            # read a lock
            lock = [0,0,0,0,0]
            for _ in range(5):
                line = f.readline()
                for p in range(5):
                    if line[p] == '#':
                        lock[p] += 1
            locks.append(lock)
        elif line[0] == '.':
            # read a key
            key = [0,0,0,0,0]
            for _ in range(5):
                line = f.readline()
                for p in range(5):
                    if line[p] == '#':
                        key[p] += 1
            keys.append(key)

        # read the separators
        line = f.readline()
        line = f.readline()
        line = f.readline()

print("PART1: ", sum( all(key[p] <= 5 - lock[p] for p in range(5)) and not \
        all(key[p] + lock[p] > 5 for p in range(5)) for lock in locks for key in keys ))
