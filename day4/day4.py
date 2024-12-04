
xmas = ['X', 'M', 'A', 'S']
mas = ['M', 'A', 'S']
wordSquare = []

def findWord(startX, startY, xDelta, yDelta, word):
    foundCount = 0
    for x in word:
        if ((startX >= 0) and (startX <= len(wordSquare[0]) - 1)) and (startY >= 0) and (startY <= len(wordSquare) - 1):
            if wordSquare[startY][startX] == x:
                foundCount += 1

        startX += xDelta
        startY += yDelta
    return (foundCount == len(word))

with open("input", "r") as f:
    for line in f.readlines():
        print(line)
        wordSquare.append(line)

foundCount = 0

print(f"XMAS {len(xmas)}")
print(f"Wordsquare rows {len(wordSquare)}")
print(f"Wordsquare cols {len(wordSquare[0])}")

for startY in range(0, len(wordSquare)):
   for startX in range(0, len(wordSquare[0])):
      if (findWord(startX, startY, 0, -1, xmas)):
         foundCount += 1
      if (findWord(startX, startY, 1, -1, xmas)):
         foundCount += 1
      if (findWord(startX, startY, 1, 0, xmas)):
         foundCount += 1
      if (findWord(startX, startY, 1, 1, xmas)):
         foundCount += 1
      if (findWord(startX, startY, 0, 1, xmas)):
         foundCount += 1
      if (findWord(startX, startY, -1, 1, xmas)):
         foundCount += 1
      if (findWord(startX, startY, -1, 0, xmas)):
         foundCount += 1
      if (findWord(startX, startY, -1, -1, xmas)):
         foundCount += 1

print(f"Total found (part 1): {foundCount}") 

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
