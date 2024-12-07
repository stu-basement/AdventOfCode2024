from collections import defaultdict

def read_input(filename):
    with open(filename) as f:
        rules = []
        updates = []
        reading_rules = True
        
        for line in f:
            line = line.strip()
            if not line:  # Empty line separates rules from updates
                reading_rules = False
                continue
                
            if reading_rules:
                # Parse rule like "47|53"
                before, after = line.split('|')
                rules.append((int(before), int(after)))
            else:
                # Parse update like "75,47,61,53,29"
                updates.append([int(x) for x in line.split(',')])
                
    return rules, updates

def is_valid_order(update, rules):
    # For each pair of numbers in the update
    for i in range(len(update)):
        for j in range(i + 1, len(update)):
            # Check if there's a rule saying j should come before i
            if (update[j], update[i]) in rules:
                return False
    return True

def get_middle_number(update):
    # For odd-length updates, return the middle number
    return update[len(update) // 2]

def build_graph(numbers, rules):
    # Build directed graph of dependencies
    graph = defaultdict(set)
    in_degree = defaultdict(int)
    
    for num in numbers:
        graph[num]  # Ensure all numbers are in graph
        
    for before, after in rules:
        if before in numbers and after in numbers:
            graph[before].add(after)
            in_degree[after] += 1
            
    return graph, in_degree

def topological_sort(numbers, rules):
    graph, in_degree = build_graph(numbers, rules)
    
    # Start with nodes that have no dependencies
    queue = [n for n in numbers if in_degree[n] == 0]
    result = []
    
    while queue:
        # Sort queue to ensure deterministic ordering when multiple nodes are available
        queue.sort(reverse=True)  # Take highest number when multiple are available
        current = queue.pop()
        result.append(current)
        
        # Update dependencies
        for next_num in graph[current]:
            in_degree[next_num] -= 1
            if in_degree[next_num] == 0:
                queue.append(next_num)
    
    return result

def solve_part1(filename):
    rules, updates = read_input(filename)
    total = 0
    
    for update in updates:
        if is_valid_order(update, rules):
            total += get_middle_number(update)
            
    return total

def solve_part2(filename):
    rules, updates = read_input(filename)
    total = 0
    
    for update in updates:
        if not is_valid_order(update, rules):
            # Sort this invalid update
            sorted_update = topological_sort(set(update), rules)
            total += get_middle_number(sorted_update)
            
    return total

if __name__ == "__main__":
    result1 = solve_part1("input")
    print(f"Part 1 - Sum of middle numbers from valid updates: {result1}")
    
    result2 = solve_part2("input")
    print(f"Part 2 - Sum of middle numbers from corrected invalid updates: {result2}") 