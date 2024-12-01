listA = []
listB = []
totalDistance = 0

f = open('input')
for line in f.readlines():
   a, b = map(int, line.split())
   listA.append(a)
   listB.append(b)

listA.sort()
listB.sort()
indexB = 0;
for valueA in listA:
   print(f"A: {valueA}, B: {listB[indexB]}, distance {listB[indexB] - valueA}")
   totalDistance += abs(listB[indexB] - valueA)
   indexB += 1

print('Starting day 1')
print(f"Total distance {totalDistance}")

print('Starting day 1 part 2')
similarity = 0
for valueA in listA:
   count = 0
   for valueB in listB:
      if valueA == valueB:
         count += 1
   similarity += (valueA * count)

print(f"Similarity score {similarity}")
