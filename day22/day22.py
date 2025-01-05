""" AdventOfCode Day 22 """
from itertools import pairwise
from more_itertools import windowed

buyerSeeds = []
bananas = {}

def nextSecret(s):
    """ Use a PRNG to generate the secret prices """
    next_s = ((s * 64) ^ s) % 16777216
    next_s = ((next_s // 32) ^ next_s) % 16777216
    next_s = ((next_s * 2048) ^ next_s) % 16777216

    return next_s

with open("input", "r", encoding="utf-8") as f:
    line = f.readline().replace('\n', '')
    while line:
        buyerSeeds.append(int(line))
        line = f.readline().replace('\n','')

# Part 1 - Simply generate 2000 secret numbers and take the total
# Part 2 - For each buyer, get all the sequences # and the total bananas they would yield
# dictionary of key: sequence, value: total bananas
bananas = {}
total_secrets = 0
for b in buyerSeeds:
    ns = b
    prices = [ ns % 10 ]
    for n in range(2000):
        ns = nextSecret(ns)
        # generate the first digits of prices
        prices.append( ns % 10 )
    total_secrets += ns

    buyerSequences = {}

    # calculate the price changes
    deltas = [str(p[1] - p[0]) for p in pairwise(prices) ]

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

print(f"PART1: Total of 2000th secrets: {total_secrets}")
print(f"PART2: Max bananas: {max(bananas.values())}")
