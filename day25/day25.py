keys = []
locks = []

with open("input", "r") as f:
    line = f.readline()
    while len(line) > 1:
        if line[0] == '#':
            # read a lock
            lock = [0,0,0,0,0]
            for l in range(5):
                line = f.readline()
                for p in range(5):
                    if line[p] == '#':
                        lock[p] += 1
            locks.append(lock)
        elif line[0] == '.':
            # read a key
            key = [0,0,0,0,0]
            for l in range(5):
                line = f.readline()
                for p in range(5):
                    if line[p] == '#':
                        key[p] += 1
            keys.append(key)

        # read the separators
        line = f.readline()
        line = f.readline()
        line = f.readline()

def keyFits(k, l):
    for p in range(5):
        if k[p] > 5 - l[p]:
            return False
    return True

def keyOverlaps(k, l):
    for p in range(5):
        if k[p] + l[p] > 5:
            return True
    return False

print(f"Locks: {locks}")
print(f"Keys: {keys}")

lockKeyPair =  0
for l in locks:
    for k in keys:
        if keyFits(k, l) and not keyOverlaps(k, l):
            lockKeyPair += 1
print(f"Total pairs: {lockKeyPair}")
