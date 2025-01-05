""" AdventOfCode Day 23 """
import networkx as nx

G = nx.Graph()

with open("input", "r", encoding="utf-8") as f:
    line = f.readline()
    while len(line) > 1:
        n = line.replace('\n', '').strip().split('-')
        G.add_edge( n[0], n[1] )
        G.add_edge( n[1], n[0] )
        line = f.readline()

# find all the 3-qliques in the graph
cliques_of_interest = [clique for clique in nx.enumerate_all_cliques(G) \
        if len(clique) == 3 and any(n.startswith("t") for n in clique)]

print(f"PART1: Total cliques of interest: {len(cliques_of_interest)}")

# find the largest clique in the graph
lan_party_cliques = list(nx.find_cliques(G))
largest_clique = max(lan_party_cliques, key=len)
largest_clique.sort()
print("PART2:", largest_clique)
