# solve with simultaneous equations
def solve(prizeX, prizeY, aDX, aDY, bDX, bDY):

    nA = ((prizeX * bDY) - (prizeY * bDX)) / ((bDY * aDX) - (bDX * aDY))
    nB = (prizeY - (nA * aDY)) / bDY

    return int(nA), int(nB)

n = 0
machines = []
with open("input", "r") as f:
    lines = f.readlines()
    while (n < len(lines)):
        buttonA = lines[n].strip()
        buttonB = lines[n+1].strip()
        prize = lines[n+2].strip()
        n += 4

        aInfo = buttonA[12:].split(',')
        aDX = int(aInfo[0])
        aDY = int(aInfo[1][3:])

        aInfo = buttonB[12:].split(',')
        bDX = int(aInfo[0])
        bDY = int(aInfo[1][3:])
        bInfo = buttonB[12:]
        prizeInfo = prize[7:].split(',')
        prizeX = int(prizeInfo[0][2:])
        prizeY = int(prizeInfo[1][3:])

        machines.append((aDX, aDY, bDX, bDY, prizeX, prizeY))

totalCost = 0
print(f"{len(machines)} machines")
for m in machines:
    aDX = m[0]
    aDY = m[1]
    bDX = m[2]
    bDY = m[3]
    prizeX = m[4]
    prizeY = m[5]

totalCost = 0
for m in machines:
    aDX = m[0]
    aDY = m[1]
    bDX = m[2]
    bDY = m[3]
    prizeX = m[4]
    prizeY = m[5]
    nA, nB = solve(prizeX, prizeY, aDX, aDY, bDX, bDY)
    # cross-check answer
    if ((nA * aDX) + (nB * bDX) == prizeX) and ((nA * aDY) + (nB * bDY) == prizeY):
        totalCost += (3 * nA) + nB

print(f"PART1 (simultaneous) Least cost to win all prizes {totalCost}")

totalCost = 0
for m in machines:
    aDX = m[0]
    aDY = m[1]
    bDX = m[2]
    bDY = m[3]
    prizeX = 10000000000000 + m[4]
    prizeY = 10000000000000 + m[5]
    nA, nB = solve(prizeX, prizeY, aDX, aDY, bDX, bDY)
    # cross-check answer
    if ((nA * aDX) + (nB * bDX) == prizeX) and ((nA * aDY) + (nB * bDY) == prizeY):
        totalCost += (3 * nA) + nB

print(f"PART2 Least cost to win all prizes {totalCost}")
