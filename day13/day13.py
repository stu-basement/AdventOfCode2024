""" AdventOfCode Day 13 """
# solve with simultaneous equations
def solve(pX, pY, dxA, dyA, dxB, dyB):
    """ Solve the for nA, nB using simultaneous equations """
    a = ((pX * dyB) - (pY * dxB)) / ((dyB * dxA) - (dxB * dyA))
    b = (pY - (a * dyA)) / dyB 

    return int(a), int(b)

n = 0
machines = []
with open("input", "r", encoding="utf-8") as f:
    lines = f.readlines()
    while n < len(lines):
        buttonA = lines[n].strip()
        buttonB = lines[n+1].strip()
        prize = lines[n+2].strip()
        n += 4

        aInfo = buttonA[12:].split(',')
        aDX = int(aInfo[0])
        aDY = int(aInfo[1][3:])

        bInfo = buttonB[12:].split(',')
        bDX = int(bInfo[0])
        bDY = int(bInfo[1][3:])
        prizeInfo = prize[7:].split(',')
        prizeX = int(prizeInfo[0][2:])
        prizeY = int(prizeInfo[1][3:])

        machines.append( (aDX, aDY, bDX, bDY, prizeX, prizeY) )

totalCost = 0
for (aDX, aDY, bDX, bDY, prizeX, prizeY) in machines:
    nA, nB = solve(prizeX, prizeY, aDX, aDY, bDX, bDY)
    # cross-check answer
    if ((nA * aDX) + (nB * bDX) == prizeX) and ((nA * aDY) + (nB * bDY) == prizeY):
        totalCost += (3 * nA) + nB

print(f"PART1 (simultaneous) Least cost to win all prizes {totalCost}")

totalCost = 0
for (aDX, aDY, bDX, bDY, prizeX, prizeY) in machines:
    prizeX += 10000000000000
    prizeY += 10000000000000
    nA, nB = solve(prizeX, prizeY, aDX, aDY, bDX, bDY)
    # cross-check answer
    if ((nA * aDX) + (nB * bDX) == prizeX) and ((nA * aDY) + (nB * bDY) == prizeY):
        totalCost += (3 * nA) + nB

print(f"PART2 Least cost to win all prizes {totalCost}")
