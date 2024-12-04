import numpy as np
from scipy.signal import convolve2d

def read_input(filename):
    with open(filename) as f:
        return [list(line.strip()) for line in f if line.strip().isalpha() and line.strip().isupper()]

def create_pattern_matrices():
    # Each pattern is a 3x3 matrix where:
    # M = 1, A = 2, S = 3, and 0 = don't care
    patterns = []
    
    # Pattern 1: M.S/.A./M.S
    p1 = np.array([
        [1, 0, 3],
        [0, 2, 0],
        [1, 0, 3]
    ])
    patterns.append(p1)
    
    # Pattern 2: S.M/.A./S.M
    p2 = np.array([
        [3, 0, 1],
        [0, 2, 0],
        [3, 0, 1]
    ])
    patterns.append(p2)
    
    # Pattern 3: M.S/.A./S.M
    p3 = np.array([
        [1, 0, 3],
        [0, 2, 0],
        [3, 0, 1]
    ])
    patterns.append(p3)
    
    # Pattern 4: S.M/.A./M.S
    p4 = np.array([
        [3, 0, 1],
        [0, 2, 0],
        [1, 0, 3]
    ])
    patterns.append(p4)
    
    return patterns

def find_xmas_patterns(grid):
    # Convert grid to numeric array
    numeric_grid = np.zeros_like(grid, dtype=int)
    numeric_grid[np.array(grid) == 'M'] = 1
    numeric_grid[np.array(grid) == 'A'] = 2
    numeric_grid[np.array(grid) == 'S'] = 3
    
    total_matches = 0
    patterns = create_pattern_matrices()
    
    for pattern in patterns:
        # Create kernel for matching
        kernel = np.ones((3, 3))
        
        # For each position that matters in the pattern
        match_positions = pattern != 0
        result = np.ones(numeric_grid.shape[0] - 2, dtype=int)
        
        # Check each position that matters
        for i in range(3):
            for j in range(3):
                if match_positions[i, j]:
                    matches = convolve2d(
                        (numeric_grid == pattern[i, j]).astype(int),
                        np.array([[1 if x == i and y == j else 0 
                                 for x in range(3)] 
                                for y in range(3)]),
                        mode='valid'
                    )
                    result = result & (matches == 1)
        
        total_matches += np.sum(result)
    
    return total_matches

def solve_part2(filename):
    grid = read_input(filename)
    return find_xmas_patterns(grid)

if __name__ == "__main__":
    result = solve_part2("input")
    print(f"Part 2: X-MAS appears {result} times in the word search") 