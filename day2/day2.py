""" AdventOfCode Day 2 """

# A safe report has successive values all increasing or decreasing
# and the difference between successive values no greater than 3
def safe_report(deltas):
    """ Check that a report is safe """
    return all(0 < abs(delta) <= 3 for delta in deltas) and \
            (all(delta < 0 for delta in deltas) or all(delta > 0 for delta in deltas))

with open("input", "r", encoding="utf-8") as f:
    total_safe = 0
    total_cleaned= 0
    for line in f.readlines():
        levels = list(map(int, line.split()))

        if safe_report(list(level1 - level0 for level1, level0 in zip(levels, levels[1:]))):
            total_safe += 1
        else:
            for t in range(1, len(levels)+1):
                oneRemoved = levels[0:t-1]+levels[t:]
                if safe_report(list(level0 - level1 \
                        for level0, level1 in zip(oneRemoved, oneRemoved[1:]))):
                    total_cleaned += 1
                    break
# Part 1
print(f"Total safe: {total_safe}")

# Part 2
print(f"Total safe: {total_safe + total_cleaned}")
