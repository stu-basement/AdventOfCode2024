from collections import defaultdict
import math
import functools

def expandStones(stones, blinks):
    for n in range(0,blinks):
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
    print(f"After blink {blinks} {len(stones)} stones {stones}")


# Use a cache to answer the question "how many stones will this become after a number of blinks
# 0 => 1     => 2024     => 20 24     => 2 0 2 4
# 1 => 2024  => 20 24    => 2 0 2 4   => 4048 1 4048 8096
# 2 => 4048  => 40 48    => 4 0 4 8   => 8096 1 8096 16192
# 3 => 6072  => 60 72    => 6 0 7 2
# 4 => 8096  => 80 96    => 8 0 9 6
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
   stones = list(map(int, line.split()))

# Part 1
print (f"Part 1 {sum(count(int(n), 0, 25) for n in stones)}")
print(count.cache_info())

# Part 2
print (f"Part 2 (cached/memoized) {sum(count(int(n), 0, 75) for n in stones)}")

# Test expansion of stones
stones = [0]
print(f"Expansion of {stones}")
expandStones(stones, 4)
stones = [1]
print(f"Expansion of {stones}")
expandStones(stones, 4)
stones = [2]
print(f"Expansion of {stones}")
expandStones(stones, 4)
stones = [5]
print(f"Expansion of {stones}")
expandStones(stones, 5)

print(f"Implement with dictionary")
f = open('input')
for line in f.readlines():
   inputStones = list(map(int, line.split()))

stones = defaultdict(int)
for s in inputStones:
    stones[s] = 1

def blink(stones):
    blinkStones = defaultdict(int)

    # If there's any zeros, tansform them to 1s in this blink and add the 0s count to the 1s count
    if 0 in stones:
        blinkStones[1] += stones[0]
        del stones[0]

    for stone, count in stones.items():

        # Stone has an even number of digits - split it
        numDigits = int(math.log10(int(stone))) + 1 
        if numDigits % 2 == 0:
            leftNum = stone // (10 ** (numDigits // 2))
            rightNum = stone - (leftNum * (10 ** (numDigits // 2)))
            blinkStones[leftNum] += count
            blinkStones[rightNum] += count
        else:
            # Multiply stone by 2024 for all other stone numbers
            blinkStones[(stone * 2024)] += count

    return blinkStones

for x in range(75):
    stones = blink(stones)

print(f"Part 2 (dictionary) {sum(stones.values())}")
print(f"Dictionary size {len(stones)}")
