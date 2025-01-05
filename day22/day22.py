""" AdventOfCode Day 22 """
from more_itertools import windowed

buyerSeeds = []
bananas = {}

def nextSecret(s):
    """ Use a PRNG to generate the secret prices """
    next_s = ((s * 64) ^ s) % 16777216
    next_s = ((next_s // 32) ^ next_s) % 16777216
    next_s = ((next_s * 2048) ^ next_s) % 16777216

    return ns

with open("input", "r", encoding="utf-8") as f:
    line = f.readline().replace('\n', '')
    while line:
        buyerSeeds.append(int(line))
        line = f.readline().replace('\n','')

# Simply generate 2000 secret numbers and take the total
total_secrets = 0
for b in buyerSeeds:
    ns = b
    for n in range(2000):
        ns = nextSecret(ns)
    total_secrets += ns
print(f"PART1: Total of 2000th secrets: {total_secrets}")

# PART 2

# For each buyer, get all the sequences
# and the total bananas they would yield
# dictionary of key: sequence, value: total bananas
bananas = {}

for b in buyerSeeds:
    buyerSequences = {}

    # generate the first digits of prices
    ns = b
    prices = [ ns % 10 ]
    for i in range(2000):
        ns = nextSecret(ns)
        prices.append( ns % 10 )

    # calculate the price changes
    deltas = [str(prices[i+1] - prices[i]) for i in range(len(prices) - 1)]

    # use a sliding window to find the pattern
    for sn, sequence in enumerate(windowed(deltas, n=4, step=1)):
        # dictionary should contain the total bananas for this buyer
        # for this sequence
        if sequence not in buyerSequences:
            buyerSequences[ sequence ] = prices[sn+4]

    # get the total sold for all matching sequences for this buyer
    for k, v in buyerSequences.items():
        if k not in bananas:
            bananas[k] = v
        else:
            bananas[k] += v

print(f"PART2: Max bananas: {max(bananas.values())}")
