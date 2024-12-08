from collections import defaultdict
from typing import List, Tuple, Set

def parse_input(input_text: str) -> List[List[str]]:
    return [list(line.strip()) for line in input_text.splitlines() if line.strip()]

def find_antennas(grid: List[List[str]]) -> defaultdict:
    # Group antennas by frequency
    antennas = defaultdict(list)
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] != '.':
                antennas[grid[y][x]].append((x, y))
    return antennas

def is_collinear(p1: Tuple[int, int], p2: Tuple[int, int], p3: Tuple[int, int]) -> bool:
    # Check if three points are in a straight line
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    return (y2 - y1) * (x3 - x1) == (y3 - y1) * (x2 - x1)

def find_antinodes_part1(antennas: defaultdict, grid_width: int, grid_height: int) -> Set[Tuple[int, int]]:
    antinodes = set()
    
    for freq, positions in antennas.items():
        if len(positions) < 2:
            continue
            
        # Check each pair of antennas
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                p1, p2 = positions[i], positions[j]
                dx = p2[0] - p1[0]
                dy = p2[1] - p1[1]
                
                # Find points at double distance on both sides
                for multiplier in [-2, 2]:
                    x = p1[0] - multiplier * dx
                    y = p1[1] - multiplier * dy
                    if 0 <= x < grid_width and 0 <= y < grid_height:
                        antinodes.add((x, y))
                    
                    x = p2[0] + multiplier * dx
                    y = p2[1] + multiplier * dy
                    if 0 <= x < grid_width and 0 <= y < grid_height:
                        antinodes.add((x, y))
    
    return antinodes

def find_antinodes_part2(antennas: defaultdict, grid_width: int, grid_height: int) -> Set[Tuple[int, int]]:
    antinodes = set()
    
    for freq, positions in antennas.items():
        if len(positions) < 2:
            continue
            
        # Check each point in the grid
        for y in range(grid_height):
            for x in range(grid_width):
                # Count how many antennas are collinear with this point
                collinear_count = 0
                for i in range(len(positions)):
                    for j in range(i + 1, len(positions)):
                        if is_collinear(positions[i], positions[j], (x, y)):
                            collinear_count += 1
                            break
                    if collinear_count > 0:
                        break
                
                if collinear_count > 0:
                    antinodes.add((x, y))
                    
        # Add antenna positions themselves if there are multiple antennas of same frequency
        if len(positions) >= 2:
            for pos in positions:
                antinodes.add(pos)
    
    return antinodes

def solve(input_text: str) -> Tuple[int, int]:
    grid = parse_input(input_text)
    grid_height = len(grid)
    grid_width = len(grid[0])
    
    antennas = find_antennas(grid)
    
    part1_antinodes = find_antinodes_part1(antennas, grid_width, grid_height)
    part2_antinodes = find_antinodes_part2(antennas, grid_width, grid_height)
    
    return len(part1_antinodes), len(part2_antinodes)

def main():
    with open('input', 'r') as f:
        input_text = f.read()
    
    part1, part2 = solve(input_text)
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == "__main__":
    main() 