import numpy as np
from scipy.signal import convolve2d

def read_input(filename):
    with open(filename) as f:
        return [list(line.strip()) for line in f if line.strip().isalpha() and line.strip().isupper()]

def create_pattern_matrices():
    # Create all possible X pattern matrices
    # Each position will be 1 for M, 2 for A, 3 for S, and 0 for don't care
    patterns = []
    
    # Base pattern template
    base = np.zeros((3, 3), dtype=int)
    base[1, 1] = 2  # Center is always 'A'
    
    # The four possible diagonal combinations:
    # M-S/M-S, M-S/S-M, S-M/M-S, S-M/S-M
    diagonals = [
        [(1,3), (1,3)],  # M-S/M-S
        [(1,3), (3,1)],  # M-S/S-M
        [(3,1), (1,3)],  # S-M/M-S
        [(3,1), (3,1)]   # S-M/S-M
    ]
    
    for d1, d2 in diagonals:
        pattern = base.copy()
        # First diagonal (top-left to bottom-right)
        pattern[0, 0] = d1[0]  # top-left
        pattern[2, 2] = d1[1]  # bottom-right
        # Second diagonal (top-right to bottom-left)
        pattern[0, 2] = d2[0]  # top-right
        pattern[2, 0] = d2[1]  # bottom-left
        patterns.append(pattern)
    
    return patterns

def convert_grid_to_numeric(grid):
    # Convert characters to numbers
    conversion = {'M': 1, 'A': 2, 'S': 3}
    return np.array([[conversion.get(c, 0) for c in row] for row in grid])

def find_xmas_patterns(grid):
    # Convert input grid to numeric matrix
    numeric_grid = convert_grid_to_numeric(grid)
    
    # Get all pattern matrices
    patterns = create_pattern_matrices()
    
    total_matches = 0
    
    # Convolve with each pattern
    for pattern in patterns:
        # Convolve and find matches
        # mode='valid' ensures we only get complete overlaps
        result = convolve2d(numeric_grid == pattern[0,0], np.ones((3,3)), mode='valid')
        for i in range(3):
            for j in range(3):
                if pattern[i,j] != 0:  # if this position matters
                    result *= (convolve2d(numeric_grid == pattern[i,j], 
                                        np.zeros((3,3), dtype=int) + np.eye(3)[i,j], 
                                        mode='valid'))
        
        total_matches += np.sum(result > 0)
    
    return total_matches

def solve_part2(filename):
    grid = read_input(filename)
    return find_xmas_patterns(grid)

if __name__ == "__main__":
    result = solve_part2("input")
    print(f"Part 2: X-MAS appears {result} times in the word search") 