""" ADventOfCode Day 24 """
import networkx as nx

# Signal states map a signal name to a value (0, 1 or ?)
signalStates = {}
gates = {}

# Signals are tuples ('name', value)
def isInputSignal(signalName):
    """ Indicate if this is an input signal x00-x99 """
    return (signalName[0] == 'x' or signalName[0] == 'y') and signalName[1:].isnumeric()

def isOutputSignal(signalName):
    """ Indicate if this is an output signal z00-z99 """
    return signalName[0] == 'z' and signalName[1:].isnumeric()

# Gates maps 'name' to a tuple (function, input1, input2, output)
def evaluateGate(g):
    """ Evaluate the output of a gate, given its input values """
    if isInputSignal(g[1]):
        input1 = signalStates[g[1]]
    else:
        input1 = gates[g[1]][3]

    if isInputSignal(g[2]):
        input2 = signalStates[g[2]]
    else:
        input2 = gates[g[2]][3]

    if input1 == '?' or input2 == '?':
        return '?'

    if g[0] == 'AND':
        return input1 & input2
    if g[0] == 'OR':
        return input1 | input2
    if g[0] == 'XOR':
        return input1 ^ input2

    return '?'

def outputSignalsToDecimal():
    """ Convert the output value bits to decimal """
    outputSignals = []
    for s in forwardG.nodes:
        if isOutputSignal(s):
            outputSignals.append(s)
    outputSignals.sort(reverse=True)
    total = gates[outputSignals[0]][3]
    for s in outputSignals[1:]:
        total = (total * 2) + gates[s][3]

    return total

def runSimulator():
    """ Run a simulation of the logic circuit """
    inputStack = []

    for s in signalStates:
        for n in forwardG.neighbors(s):
            inputStack.append(n)

    while inputStack:
        node = inputStack.pop()
        gate = gates[node]

        outputSignal = evaluateGate(gate)
        gates[node] = (gate[0], gate[1], gate[2], outputSignal)
        signalStates[node] = outputSignal

        signalIter = forwardG.neighbors(node)
        for n in signalIter:
            if not isInputSignal(n):
                inputStack.append( n )

# nodes in the graph are gates or signals
# edges connect nodes
forwardG = nx.DiGraph()
backwardG = nx.DiGraph()

with open("input", "r", encoding="utf-8") as f:
    # add the signal inputs and outputs
    line = f.readline().replace('\n', '')
    while len(line) > 1:
        signal = line.split(':')
        signalStates[signal[0]] = int(signal[1])
        forwardG.add_node( signal[0] )
        backwardG.add_node( signal[0] )
        line = f.readline().replace('\n', '')

    # add the gates
    line = f.readline().replace('\n', '')
    while len(line) > 1:
        wiring = line.split(' ')
        gates[wiring[4]] = ( wiring[1], wiring[0], wiring[2], '?' )

        # gate outputs could go to signals (which we've already added)
        # or to gates which we might not have found yet
        # gates are named for their output
        # there is an edge from each input to this node
        # there is an edge from this node to another node
        # which is not an output signal
        forwardG.add_node( wiring[4] )
        forwardG.add_edge( wiring[0], wiring[4] )
        forwardG.add_edge( wiring[2], wiring[4] )

        # for tracing faults, add edges from output to input
        backwardG.add_node( wiring[4])
        backwardG.add_edge( wiring[4], wiring[0] )
        backwardG.add_edge( wiring[4], wiring[2] )

        line = f.readline().replace('\n', '')

runSimulator()
print(f"Output number: {outputSignalsToDecimal()}")

# Plan for part 2 - test each part of the circuit to determine fault and working adders
# there is one half-adder x00, y00 => z00
# then the remainder are 1-bit adders with carry in and carry out
