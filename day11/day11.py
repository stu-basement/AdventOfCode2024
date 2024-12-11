import math
import functools

f = open('input')
for line in f.readlines():
   stones = list(map(int, line.split()))

# Part 1
for n in range(0,25):
    i = 0
    numStones = len(stones)
    while (i < numStones):
        if (stones[i] == 0):
            numDigits = 1
        else:
            numDigits = int(math.log10(stones[i]))+1

        if (numDigits % 2) == 0:
            leftNum = stones[i] // (10 ** (numDigits // 2))
            rightNum = stones[i] - (leftNum * (10 ** (numDigits // 2)))
            stones[i] = leftNum
            stones.insert(i+1, rightNum)
            numStones += 1
            i += 1
        else:
            if (stones[i] == 0):
                stones[i] = 1
            else:
                stones[i] *= 2024
        i += 1
    print(f"After blink {n+1} {len(stones)} stones")

# Part 2
@functools.cache
def count(n, b):
    if (b == 75):
        return 1
    if (n == 0):
        return count(1, b + 1)

    numDigits = int(math.log10(n)) + 1
    if numDigits % 2 == 0:
        leftNum = n // (10 ** (numDigits // 2))
        rightNum = n - (leftNum * (10 ** (numDigits // 2)))
        return count(leftNum, b + 1) + count(rightNum, b + 1)
    return count(n * 2024, b + 1)

print ( sum(count(int(n), 0) for n in open("input").read().split()))

n = 1234
ns = str(n)
nl = len(ns)
print (ns[:nl//2] + ns[nl // 2 :])

