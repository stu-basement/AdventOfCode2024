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

# dictionary of key: (input1, input2, function) to value: output
connections = {}
with open("input", "r", encoding="utf-8") as f:
    # add the signal inputs and outputs
    line = f.readline().replace('\n', '')
    while len(line) > 1:
        signal = line.split(':')
        signalStates[signal[0]] = int(signal[1])
        forwardG.add_node( signal[0] )
        line = f.readline().replace('\n', '')

    # add the gates
    line = f.readline().replace('\n', '')
    while len(line) > 1:
        wiring = line.split(' ')
        # gates are outputName: (gate function, input1, input2)
        # for gate inputs, order them alphabetically to make lookups consistent
        gates[wiring[4]] = ( wiring[1], \
                wiring[0] if wiring[0] <= wiring[2] else wiring[2], \
                wiring[2] if wiring[2] > wiring[0] else wiring[0], '?' )

        # connections are (input1, input2, function): output
        connections[ (wiring[0] if wiring[0] <= wiring[2] else wiring[2], \
                wiring[2] if wiring[2] > wiring[0] else wiring[0], \
                wiring[1]) ] = wiring[4]

        # gate outputs could go to signals (which we've already added)
        # or to gates which we might not have found yet
        # gates are named for their output
        # there is an edge from each input to this node
        # there is an edge from this node to another node
        # which is not an output signal
        forwardG.add_node( wiring[4] )
        forwardG.add_edge( wiring[0], wiring[4] )
        forwardG.add_edge( wiring[2], wiring[4] )

        line = f.readline().replace('\n', '')

runSimulator()
print(f"Output number: {outputSignalsToDecimal()}")

# Plan for part 2 - test each part of the circuit to determine fault and working adders
# there is one half-adder x00, y00 => z00
# then the remainder are 1-bit adders with carry in and carry out
# all inputs x00, y00 should connect to an XOR and an AND
# all outputs z00 should come from an XOR
# all carry out should come from an AND and either go to an output
# or to an XOR and an AND
# Substitute the signal names with these to make checking easier
#
# Half-Adder:
# The half-adder has 2 gates
# z00 XOR x00, y00 (must exist, verify input connections)
# carryout00 AND x00, y00 (substitute carryout00 for gate output)
#
# Full-Adder:
# Every 1-bit adder has 5 gates
# znn XOR xnnynnXOR, carrynn (must exist, substitute "carrynn", "xnnynnXOR" for input1 and input2)
# xnnynnXOR XOR xnn, ynn (can verify input connections)
# xnnynnAND AND xnn, ynn (substitute xnnynnAND for gate output)
# xnnynncarrynnAND AND xnynnXOR, carrynn (substitute xnnynncarrynnAND for gate output)
# carryout(n-1)(n-1) OR xnnynnAND, xnnynncarrynnAND (substitute carryout(n-1)(n-1) for gate output)
# Verify that carrynn = carryout(n-1)(n-1) for all nn > 0

# Check for inconsistencies in the wiring
# We dont care which order inputs to gates go,
# e.g x00 XOR y00 is the same as y00 XOR x00 in the wiring list
# but we do care if an output goes to the wrong gate
# e.g. for adder 0, output goes to z01 instead of z00
def orderedInputs(a, b, f):
    if a < b:
        return a, b, f
    else:
        return b, a, f

anomalies = set()

# check AND gates
print("Check AND gates")
for k, v in gates.items():
    # check for input anomalies
    if v[0] == "AND":
        gate_input1 = v[1]
        if not isInputSignal(gate_input1):
            if gates[gate_input1][0] == "AND" \
                    and gates[gate_input1][1] != 'x00'\
                    and gates[gate_input1][2] != 'y00':
                anomalies.add( k )

        gate_input2 = v[2]
        if not isInputSignal(gate_input2):
            if gates[gate_input2][0] == "AND" \
                    and gates[gate_input2][1] != 'x00'\
                    and gates[gate_input2][2] != 'y00':
                anomalies.add( k )

        # check for output anomalies
        for n in forwardG.neighbors(k):
            gate_inputs = {gate_input1, gate_input2}
            if gates[n][0] != "OR" and not isOutputSignal(n) \
                    and not ("x00" in gate_inputs or "y00" in gate_inputs):
                anomalies.add( k )

# check XOR gates
print("Check XOR gates")
for k, v in gates.items():
    # check for input anomalies
    if v[0] == "XOR":
        gate_input1 = v[1]
        if not isInputSignal(gate_input1) \
                and gates[gate_input1][1] != 'x00'\
                and gates[gate_input1][2] != 'y00':
            if gates[gate_input1][0] == "AND":
                anomalies.add( k )

        gate_input2 = v[2]
        if not isInputSignal(gate_input2):
            if gates[gate_input2][0] == "AND" \
                and gates[gate_input2][1] != 'x00'\
                and gates[gate_input2][2] != 'y00':
                anomalies.add( k )

        # check output anomalies
        for n in forwardG.neighbors(k):
            if not isOutputSignal(n):
                if gates[n][0] != "AND" and gates[n][0] != "XOR":
                    anomalies.add( k )

# Check OR gates
print("Check OR gates")
for k, v in gates.items():
    # check for input anomalies
    if v[0] == "OR":
        gate_input1 = v[1]
        gate_input2 = v[2]
        if gates[gate_input1][0] != "AND" and gates[gate_input2] != "AND":
            anomalies.add( k )

        # check output anomalies
        for n in forwardG.neighbors(k):
            if not isOutputSignal(n):
                if gates[n][0] != "AND" and gates[n][0] != "XOR":
                    anomalies.add( k )

# Check outputs
for z in signalStates:
    if isOutputSignal(z) and z in gates:
        if gates[z][0] != "XOR" and z != 'z45':
            anomalies.add( z )

print(f"Anomalies: {anomalies}")

anomalies = set()
valid = set()

carryIn = None
for g in forwardG.neighbors('x00'):
    if gates[g][0] == "AND":
        carryIn = g

# Check from inputs forward
for a in range(1, 44):
    xSignal = 'x' + str(a).zfill(2)
    ySignal = 'y' + str(a).zfill(2)
    carryOut = None

    first_gates = forwardG.neighbors(xSignal)
    for gate in first_gates:
        if gates[gate][0] == "AND":
            xyAND = gate
            if isOutputSignal(xyAND):
                anomalies.add( (a, xyAND) )
            else:
                second_gate = forwardG.neighbors(xyAND)
                carryOut = next(second_gate)
                if gates[carryOut][0] == "OR":
                    valid.add( (a, xyAND) )
                else:
                    anomalies.add( (a, xyAND) )
        else:
            xyXOR = gate
            if isOutputSignal(xyXOR):
                anomalies.add( (a, xyXOR) )
            else:
                second_gates = forwardG.neighbors(xyXOR)
                validXOR = False
                validAND = False
                for g in second_gates:
                    if not validXOR:
                        validXOR = gates[g][0] == "XOR"
                    if not validAND:
                        validAND = gates[g][0] == "AND"
                if validXOR and validAND:
                    valid.add( (a, xyXOR) )
                else:
                    anomalies.add( (a, xyXOR) )

    if (a, xyXOR) in valid:
        second_gates = forwardG.neighbors(xyXOR)
        for gate in second_gates:
            if gates[gate][0] == "XOR":
                zSignal = gate
                if not isOutputSignal(gate):
                    anomalies.add( (a, zSignal) )
                else:
                    gate_inputs = {gates[gate][1], gates[gate][2]}
                    if carryIn in gate_inputs:
                        valid.add( (a, carryIn) )
                    else:
                        anomalies.add( (a, carryIn) )

            if gates[gate][0] == "AND":
                xyXORcarryInAND = gate
                gate_inputs = {gates[gate][1], gates[gate][2]}
                if carryIn in gate_inputs:
                    valid.add( (a, carryIn) )

                third_gates = forwardG.neighbors(xyXORcarryInAND)
                for gate in third_gates:
                    if gates[gate][0] == "OR":
                        if not isOutputSignal(gate):
                            gate_inputs = {gates[gate][1], gates[gate][2]}
                            if xyAND in gate_inputs:
                                valid.add( (a, xyXORcarryInAND) )
                                carryOut = gate
    zSignal = 'z' + str(a).zfill(2)
    if gates[zSignal][0] != "XOR":
        anomalies.add( (a, zSignal) )
    carryIn = carryOut

print(f"Anomalies: {anomalies}")
