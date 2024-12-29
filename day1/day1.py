from collections import Counter

listA = []
listB = []

with open("input", "r") as f:
    for line in f.readlines():
        a, b = map(int, line.replace('\n', '').split())
        listA.append(a)
        listB.append(b)

# Part 1
listA.sort()
listB.sort()
oneList = zip(listA, listB)
totalDistance = sum([abs(x[1] - x[0]) for x in oneList])

print(f"Total distance {totalDistance}")

# Part 2
# Use a counter to avoid exploding time complexity to O(n^2) using B.count(a)
# https://www.reddit.com/r/adventofcode/comments/1h3vp6n/comment/lzw63fl/
cnt = Counter(listB)
similarity = sum([x * cnt[x] for x in listA])

print(f"Similarity score {similarity}")
