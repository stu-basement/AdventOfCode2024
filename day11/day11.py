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

# Use a cache to answer the question "how many stones will this become after a number of blinks
# 0 => 1 => 2024 => 20 24 => 2 0 2 4
# 2 => 4048 => 40 48 => 4 0 4 8
# 3 => 6072 => 60 72 => 6 0 7 2
# 4 => 8096 => 80 96 => 8 0 9 6
# 5 => 10120 => 20482880 => 2048 2880 => 20 48 28 80 => 2 0 4 8 2 8 8 0
# 6 => 12144 => 24579456 => 2457 9456 => 24 57 94 56 => 2 4 5 7 9 4 5 6
# 8 => 16192 => 32772608 => 3277 2608 => 32 77 26 08 => 3 2 7 7 2 6 0 8
# 9 => 18216 => 36869184 => 3686 9184 => 36 86 91 84 => 3 6 8 6 9 1 8 4
# We can cache and calculate all of these expansions
# xx => x x (10-99)
# xxx => xxx * 2024
# xxxx => xx xx => x x
# And so on.

@functools.cache
def count(stone, blink, maxBlink):
    if (blink == maxBlink):
        return 1
    if (stone == 0):
        return count(1, blink + 1, maxBlink)

    numDigits = int(math.log10(stone)) + 1
    if numDigits % 2 == 0:
        leftNum = stone // (10 ** (numDigits // 2))
        rightNum = stone - (leftNum * (10 ** (numDigits // 2)))
        return count(leftNum, blink + 1, maxBlink) + count(rightNum, blink + 1, maxBlink)
    return count(stone * 2024, blink + 1, maxBlink)

f = open('input')
for line in f.readlines():
   stones = line.split()

print (sum(count(int(n), 0, 75) for n in stones))

stones = [0]
print (sum(count(int(n), 0, 4) for n in stones))
stones = [1]
print (sum(count(int(n), 0, 4) for n in stones))
stones = [5]
print (sum(count(int(n), 0, 5) for n in stones))

