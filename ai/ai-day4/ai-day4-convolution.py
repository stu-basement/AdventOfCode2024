import numpy as np
from scipy.signal import convolve2d

def read_input(filename):
    with open(filename) as f:
        return [list(line.strip()) for line in f if line.strip().isalpha() and line.strip().isupper()]

def create_pattern_matrices():
    # Each pattern is a 3x3 matrix where:
    # M = 1, A = 2, S = 3, and 0 = don't care
    patterns = []
    
    # All valid diagonal combinations
    diagonals = [
        # First diagonal (tl-br), Second diagonal (tr-bl)
        ('MS', 'MS'),  # M.S/.A./M.S
        ('SM', 'SM'),  # S.M/.A./S.M
        ('MS', 'SM'),  # M.S/.A./S.M
        ('SM', 'MS'),  # S.M/.A./M.S
    ]
    
    for d1, d2 in diagonals:
        pattern = np.zeros((3, 3), dtype=int)
        pattern[1, 1] = 2  # Center is always A
        
        # Set first diagonal (top-left to bottom-right)
        pattern[0, 0] = 1 if d1.startswith('M') else 3
        pattern[2, 2] = 3 if d1.endswith('S') else 1
        
        # Set second diagonal (top-right to bottom-left)
        pattern[0, 2] = 1 if d2.startswith('M') else 3
        pattern[2, 0] = 3 if d2.endswith('S') else 1
        
        patterns.append(pattern)
    
    return patterns

def find_xmas_patterns(grid):
    # Convert grid to numeric array
    numeric_grid = np.zeros(np.array(grid).shape, dtype=int)
    numeric_grid[np.array(grid) == 'M'] = 1
    numeric_grid[np.array(grid) == 'A'] = 2
    numeric_grid[np.array(grid) == 'S'] = 3
    
    total_matches = 0
    patterns = create_pattern_matrices()
    
    for pattern in patterns:
        # Create result array of proper size
        result = np.ones((numeric_grid.shape[0] - 2, numeric_grid.shape[1] - 2), dtype=int)
        
        # Check each position that matters in the pattern
        match_positions = pattern != 0
        for i in range(3):
            for j in range(3):
                if match_positions[i, j]:
                    # Create position-specific kernel
                    kernel = np.zeros((3, 3))
                    kernel[i, j] = 1
                    
                    # Convolve to find matches for this position
                    matches = convolve2d(
                        (numeric_grid == pattern[i, j]).astype(int),
                        kernel,
                        mode='valid'
                    )
                    
                    # Combine with previous results
                    result = result & (matches == 1)
        
        # Add matches found with this pattern
        total_matches += np.sum(result)
    
    return total_matches

def solve_part2(filename):
    grid = read_input(filename)
    return find_xmas_patterns(grid)

if __name__ == "__main__":
    result = solve_part2("input")
    print(f"Part 2: X-MAS appears {result} times in the word search") 