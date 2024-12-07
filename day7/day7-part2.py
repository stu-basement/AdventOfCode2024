import itertools
import math

results = []
values = []
operations = []
success = []

def operatorCombo(op, n):
   yield from itertools.product(*([op] * n))

def calc(op, term1, term2):
    if (op[0] == "+"):
      return term1 + term2
    elif (op[0] == "*"):
        return term1 * term2
    elif (op[0] == "|"):
        return (term1 * (10 ** math.floor(math.log10(term2)))) + term2
    else:
        return None

f = open('input')
count = 0
maxTerms = 0
for line in f.readlines():
    x = line.partition(":")
    results.append(int(x[0]))
    terms = list(map(int, x[2].split()))
    values.append(terms)
    maxTerms = max(maxTerms, len(terms))

for opLength in range(0, maxTerms - 1):
    for operators in operatorCombo("+*|",opLength+1):
        operations.append(list(''.join(operators)))

def calcEquation(values, combo, expectedResult):
    result= values[0]
    for v in range(1, len(values)):
        result = calc(combo[v-1], result, values[v])
    return (result == expectedResult)

value = 0
for r in range(0, len(results)):
    validResult = False
    for combo in operations:
        if (len(combo) == len(values[r]) - 1):
            validResult = calcEquation(values[r], combo, results[r])
            if (validResult):
                success.append(results[r])
                break

total = 0
print(f"SUCCESS: {success}")
print(f"Valid results {len(success)}")
for s in success:
    total += s
print(f"PART1 total calibration result {total}")
