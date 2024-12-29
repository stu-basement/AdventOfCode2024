def safeReport(levels):
    prevLevel = levels[0]
    prevDelta = levels[1] - levels[0]
    safe = True
    for l in range(1, len(levels)):
       delta = levels[l] - prevLevel
       safe = safe and (delta != 0) and (abs(delta) <= 3) and (((prevDelta < 0) and (delta < 0)) or ((prevDelta > 0) and (delta > 0)))
       prevDelta = delta
       prevLevel = levels[l]
    return safe

f = open('input')
totalSafe = 0
totalSafeAfterCleaning = 0
for line in f.readlines():
    levels = list(map(int, line.split()))


    if (safeReport(levels)):
        totalSafe += 1
    else:
        print(f"Unsafe ({len(levels)} levels")
        for t in range(0, len(levels)):
            tempLevels = levels.copy()
            print(f"Remove level {t} of {len(tempLevels)} originally {len(levels)}")
            del tempLevels[t]
            if (safeReport(tempLevels)):
               print(f"Report now safe")
               totalSafeAfterCleaning += 1
               break

# Part 1

# Part 2
print(f"Total safe: {totalSafe}")
print(f"Total safe: {totalSafe + totalSafeAfterCleaning}")
