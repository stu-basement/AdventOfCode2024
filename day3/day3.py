f = open('cleanedinput')
total = 0
for line in f.readlines():
   a, b = map(int, line.split(","))
   if (a > 999 or b > 999):
      print("Out of range")
      break
   total += (a*b)

print(f"Total (part 1): {total}")

f = open('doinput')
totalDo = 0
for line in f.readlines():
   a, b = map(int, line.split(","))
   if (a > 999 or b > 999):
      print("Out of range")
      break
   totalDo += (a*b)

f = open('dontinput')
totalDont = 0
for line in f.readlines():
   a, b = map(int, line.split(","))
   if (a > 999 or b > 999):
      print("Out of range")
      break
   totalDont += (a*b)

print(f"Total (part 2): {totalDo} excluded {totalDont}")
if (total == totalDo + totalDont):
   print("Correct: Do + Don't = original total")
