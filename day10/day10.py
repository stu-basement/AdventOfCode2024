""" AdventOfCode Day 10 """
import networkx as nx

# up, right, down, left
directions = [[0, -1], [1, 0], [0,1], [-1,0]]

# PART 1
G = nx.DiGraph()

areaMap = []
map_height = 0
trailheads = set()
tops = set()
with open("input", "r", encoding="utf-8") as f:
    line = f.readline().replace('\n', '')
    while line:
        for x, n in enumerate(list(map(int, line))):
            if n == 0:
                trailheads.add( (x, map_height, n) )
            elif n == 9:
                tops.add( (x, map_height, n) )
            G.add_node( (x, map_height, n) )
        line = f.readline().replace('\n', '')
        map_height += 1

G.add_edges_from( ( (x,y,node), (x+dx, y+dy, node+1) ) \
        for (x, y, node) in G.nodes \
        for dx,dy in directions if (x+dx, y+dy, node+1) in G)

# Part 1 answer is the total number of tops reachable from all trailheads
totalScore = sum(t in nx.dfs_preorder_nodes(G, tr, depth_limit=9) \
        for tr in trailheads for t in tops)
print(f"PART1 Trailhead score {totalScore}")

totalScore = sum(t in path for tr in trailheads \
        for path in nx.all_simple_paths(G, source=tr, target=tops) for t in tops)
print(f"PART2 Trailhead rating {totalScore}")
