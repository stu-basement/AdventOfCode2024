import networkx as nx

# Signal states map a signal name to a vale (0, 1 or ?)
signalStates = dict()

# Signals are tuples ('name', value)
def isInputSignal(signalName):
    return (signalName[0] == 'x' or signalName[0] == 'y') and signalName[1:].isnumeric()

def isOutputSignal(signalName):
    return signalName[0] == 'z' and signalName[1:].isnumeric()

def isSignal(signalName):
    return inputSignal(signalName) or outputSignal(signalName)

gates = dict()
# Gates maps 'name' to a tuple (function, input1, input2, output)
def evaluateGate(gateName, g):
    print(f"Evaluate gate {gateName} {g}")

    if isInputSignal(g[1]):
        input1 = signalStates[g[1]]
        print(f"Use signal state {input1}")
    else:
        input1 = gates[g[1]][3]
        print(f"Use gate {gates[g[1]][3]} output {input1}")

    if isInputSignal(g[2]):
        input2 = signalStates[g[2]]
        print(f"Use signal state {input2}")
    else:
        input2 = gates[g[2]][3]
        print(f"Use gate {gates[g[2]][3]} output {input2}")

    print(f"Evaluate gate {gateName} {g} with {input1} {g[0]} {input2}")
    if input1 == '?' or input2 == '?':
        print(f"Both outputs unknown")
        return '?'
    else:
        if g[0] == 'AND':
            print(f"Output {input1 & input2}")
            return input1 & input2
        elif g[0] == 'OR':
            print(f"Output {input1 | input2}")
            return input1 | input2
        elif g[0] == 'XOR':
            print(f"Output {input1 ^ input2}")
            return input1 ^ input2
    print(f"Unknown gate function")
    return '?'

def runSimulator():
    inputStack = []

    for s in signalStates:
        for n in G.neighbors(s):
            inputStack.append(n)

    while len(inputStack):
        node = inputStack.pop()
        print(f"Process gate {node}")
        gate = gates[node]

        outputSignal = evaluateGate(node, gate)
        gates[node] = (gate[0], gate[1], gate[2], outputSignal)
        print(f"Gate {gates[node]} now has value {gates[node][3]}")
        signalStates[node] = outputSignal

        signalIter = G.neighbors(node)
        for n in signalIter:
            if not isInputSignal(n):
                print(f"Signal {node} connects to {n}, add them to stack")
                inputStack.append( n )

    outputSignals = []
    outputSignalValues = []
    for s in G.nodes:
        if isOutputSignal(s):
            print(f"Output signal {s} has value {gates[s][3]}")
            outputSignals.append(s)
    outputSignals.sort(reverse=True)
    print(f"Output signals: {','.join(outputSignals)}")

    total = gates[outputSignals[0]][3]
    for s in outputSignals[1:]:
        total = (total * 2) + gates[s][3]

    print(f"Output number: {total}")

# nodes in the graph are gates or signals
# edges connect nodes
G = nx.DiGraph()

with open("input", "r") as f:

    # add the signal inputs and outputs
    line = f.readline().replace('\n', '')
    while len(line) > 1:
        signal = line.split(':')
        signalStates[signal[0]] = int(signal[1])
        G.add_node( signal[0] )
        line = f.readline().replace('\n', '')

    # add the gates
    line = f.readline().replace('\n', '')
    while len(line) > 1:
        wiring = line.split(' ')
        gates[wiring[4]] = ( wiring[1], wiring[0], wiring[2], '?' )
        print(f"{wiring[4]} = {wiring[0]} {wiring[1]} {wiring[2]}")

        # gate outputs could go to signals (which we've already added)
        # or to gates which we might not have found yet
        # gates are named for their output
        # there is an edge from each input to this node
        # there is an edge from this node to another node
        # which is not an output signal
        G.add_node( wiring[4] )
        G.add_edge( wiring[0], wiring[4] )
        G.add_edge( wiring[2], wiring[4] )

        line = f.readline().replace('\n', '')

print("Nodes:")
print(G.nodes)

print("Edges:")
print(G.edges)

print("Signals:")
print(signalStates)

print("Gates:")
print(gates)

runSimulator()
