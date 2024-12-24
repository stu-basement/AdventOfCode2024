buyerSeeds = []
bananas = {}

def mix(s, n):
    return n ^ s

def prune(n):
    return n % 16777216

def nextSecret(s):
    ns = ((s * 64) ^ s) % 16777216
    ns = ((ns // 32) ^ ns) % 16777216
    ns = ((ns * 2048) ^ ns) % 16777216

    return ns

with open("input", "r") as f:
    line = f.readline()
    while (len(line) > 1):
        buyerSeeds.append(int(line.replace('\n', '')))
        line = f.readline()

# PART 2

# For each buyer, get all the sequences
# and the total bananas they would yield 
# dictionary of key: sequence, value: total bananas
bananas = {}

for b in buyerSeeds:
    buyerSequences = {}

    # generate the secret numbers
    ns = b
    prices = [ ns ]
    for i in range(2000):
        ns = nextSecret(ns)
        prices.append(ns)

    # generate the first digits (prices)
    firstDigits = [x % 10 for x in prices]

    # calculate the price changes
    deltas = [firstDigits[i+1] - firstDigits[i] for i in range(len(firstDigits) - 1)]

    for i in range(len(deltas) - 3):
        sequence = str(deltas[i])+str(deltas[i+1])+str(deltas[i+2])+str(deltas[i+3])

        # dictionary should contain the total bananas for this buyer
        # for this sequence
        if sequence not in buyerSequences:
            buyerSequences[ sequence ] = firstDigits[i+4]

    for k, v in buyerSequences.items():
        if k not in bananas:
            bananas[k] = v
        else:
            bananas[k] += v

print(f"Max bananas: {max(bananas.values())}")
