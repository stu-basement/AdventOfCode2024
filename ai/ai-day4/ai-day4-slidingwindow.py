import numpy as np
from scipy.signal import convolve2d

def read_input(filename):
    with open(filename) as f:
        return [list(line.strip()) for line in f if line.strip().isalpha() and line.strip().isupper()]

def create_pattern_matrices():
    # Create all possible X pattern matrices
    patterns = []
    
    # The four possible diagonal combinations for M and S
    diagonals = [
        [(1,3), (1,3)],  # M-S/M-S
        [(1,3), (3,1)],  # M-S/S-M
        [(3,1), (1,3)],  # S-M/M-S
        [(3,1), (3,1)]   # S-M/S-M
    ]
    
    for d1, d2 in diagonals:
        pattern = np.zeros((3, 3), dtype=int)
        # Set the center A
        pattern[1, 1] = 2
        # Set first diagonal (top-left to bottom-right)
        pattern[0, 0] = d1[0]
        pattern[2, 2] = d1[1]
        # Set second diagonal (top-right to bottom-left)
        pattern[0, 2] = d2[0]
        pattern[2, 0] = d2[1]
        patterns.append(pattern)
    
    return patterns

def convert_grid_to_numeric(grid):
    conversion = {'M': 1, 'A': 2, 'S': 3}
    return np.array([[conversion.get(c, 0) for c in row] for row in grid])

def find_xmas_patterns(grid):
    numeric_grid = convert_grid_to_numeric(grid)
    patterns = create_pattern_matrices()
    total_matches = 0
    
    for pattern in patterns:
        # Create binary masks for each value (M=1, A=2, S=3)
        matches = np.ones(numeric_grid.shape[0] - 2, dtype=int)
        for i in range(numeric_grid.shape[1] - 2):
            window = numeric_grid[0:3, i:i+3]  # Get 3x3 window
            match = True
            for r in range(3):
                for c in range(3):
                    if pattern[r,c] != 0:  # if this position matters
                        if pattern[r,c] != window[r,c]:
                            match = False
                            break
                if not match:
                    break
            if match:
                total_matches += 1
            
        # Slide the window down
        for j in range(1, numeric_grid.shape[0] - 2):
            window = numeric_grid[j:j+3, 0:3]  # Get 3x3 window
            for i in range(numeric_grid.shape[1] - 2):
                window = numeric_grid[j:j+3, i:i+3]
                match = True
                for r in range(3):
                    for c in range(3):
                        if pattern[r,c] != 0:  # if this position matters
                            if pattern[r,c] != window[r,c]:
                                match = False
                                break
                    if not match:
                        break
                if match:
                    total_matches += 1
    
    return total_matches

def solve_part2(filename):
    grid = read_input(filename)
    return find_xmas_patterns(grid)

if __name__ == "__main__":
    result = solve_part2("input")
    print(f"Part 2: X-MAS appears {result} times in the word search") 