""" AdventOfCode Day 4 """
from collections import defaultdict

xmas = ['X', 'M', 'A', 'S']
mas = ['M', 'A', 'S']
wordSquare = []
directions = [ [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1] ]

def findWord(startX, startY, xDelta, yDelta, word):
    foundCount = 0
    for x in word:
        if ((startX >= 0) and (startX <= len(wordSquare[0]) - 1)) and (startY >= 0) and (startY <= len(wordSquare) - 1):
            if wordSquare[startY][startX] == x:
                foundCount += 1

        startX += xDelta
        startY += yDelta
    return (foundCount == len(word))

foundCount = 0
x_spots= set()
letter_spots = set()
y = 0
with open("input", "r", encoding="utf-8") as f:
    line = list(f.readline().replace('\n', ''))
    while len(line) > 0:
        for x in enumerate(line):
            if x[1] == 'X':
                x_spots.add( ( x[0], y ) )
            elif x[1] != '.':
                letter_spots.add( (x[1], x[0], y) )

        line = list(f.readline().replace('\n', ''))
        y += 1

for spot in x_spots:
    for d in directions:
        for letter in enumerate(mas):
            if (letter[1], \
                    spot[0] + (d[0] * (letter[0] + 1)), \
                    spot[1] + (d[1] * (letter[0] + 1)) ) not in letter_spots:
                break

            if letter[0] == len(mas) - 1:
                foundCount += 1

print(f"PART1: total found {foundCount}")
exit()

print("Part 2")
foundCount = 0
for startY in range(0, len(wordSquare)):
   for startX in range(0, len(wordSquare[0])):
      # Find MAS on diagonal up-right
      if (findWord(startX, startY, 1, -1, mas)):
         # MATCH if MAS found on diagonal down-right
         if (findWord(startX, startY - 2, 1, 1, mas)):
            foundCount += 1

         # MATCH if MAS found on diagonal up-left
         if (findWord(startX + 2, startY, -1, -1, mas)):
            foundCount += 1

      # Find MAS on diagonal down-right
      if (findWord(startX, startY, 1, 1, mas)):
         # MATCH if MAS found on diagonal down-left
         if (findWord(startX + 2, startY, -1, 1, mas)):
             foundCount += 1
 
         # MATCH if MAS found on diagonal up-right
         if (findWord(startX, startY + 2, 1, -1, mas)):
             foundCount += 1

      # Find MAS on diagonal down-left
      if (findWord(startX, startY, -1, 1, mas)):
         # MATCH if MAS found on diagonal up-left
         if (findWord(startX, startY+2, -1, -1, mas)):
             foundCount += 1
         # MATCH if MAS found on diagonal down-right
         if (findWord(startX - 2, startY, 1, 1, mas)):
             foundCount += 1

      # Find MAS on diagonal up-left
      if (findWord(startX, startY, -1, -1, mas)):
         # MATCH if MAS found on diagonal down-left
         if (findWord(startX, startY-2, -1, 1, mas)):
             foundCount += 1
         # MATCH if MAS found on diagonal up-right 
         if (findWord(startX-2, startY, 1, -1, mas)):
             foundCount += 1

# We match both directions of patterns, so answer is total found divided by two
print(f"Total found (part 2): {foundCount // 2}") 
