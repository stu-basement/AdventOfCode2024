""" AdventOfCode Day 7 """
import math

def findSolution(eqs, operators):
    """ find a solution to an equation by using *, +, | operators """
    # Work backwards to prune the number of possibilities
    # Process terms in reverse order
    # At each step, record the partial result and stop when this becomes zero (solution found)
    # concatenation is only possible if the last digits of the partial result
    # are the same as the last digits of the next term
    # multiplication is only possible if the partial result is exactly divisible by the next term
    # addition is only possible if subtracting the next term leads to a positive result
    # Node: (partial result, [remaining terms] )
    calibration_result = 0
    for partial, terms in eqs:
        result = partial
        stack = []

        current = (result, terms)
        stack.append(current)

        while stack:
            partial, terms = stack.pop()

            # if our partial result becomes zero and we have used all the terms,
            # this sequence is a correct solution
            if partial == 0 and not terms:
                calibration_result += result
                break

            if not terms:
                continue

            next_term = terms[0]
            for combo in operators:
                # can't have concatenation if last digits of result not same as term
                if combo == '|':
                    if (partial - next_term) % \
                            (10 ** (math.floor(math.log10(next_term)) + 1)) != 0:
                        continue
                    next_node =  ( (partial - next_term) // \
                        (10 ** (math.floor(math.log10(next_term)) + 1)), terms[1:])
                    stack.append(next_node)

                # can't have multiplication if result not exactly divisible by term
                if combo == '*':
                    if partial % next_term != 0:
                        continue
                    next_node = (partial // next_term, terms[1:])
                    stack.append(next_node)

                # can't have addition if subtraction would result in a negative number
                if combo == '+':
                    if partial - next_term < 0:
                        continue
                    next_node = (partial - next_term, terms[1:])
                    stack.append(next_node)
    return calibration_result

equations = []
with open('input', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        x = line.replace('\n', '').split(':')
        t = list(map(int, x[1].split()))
        t.reverse()
        equations.append( (int(x[0]), t) )

print(f"PART1 total calibration result {findSolution(equations, '*+')}")
print(f"PART2 total calibration result {findSolution(equations, '*+|')}")
