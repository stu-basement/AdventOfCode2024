def read_input(filename):
    with open(filename) as f:
        # Skip the problem description and get only the grid
        lines = f.readlines()
        grid = []
        for line in lines:
            # Only process lines that are all uppercase letters
            if line.strip().isalpha() and line.strip().isupper():
                grid.append(list(line.strip()))
    return grid

def count_xmas(grid):
    rows = len(grid)
    cols = len(grid[0])
    count = 0
    
    # All possible directions: right, down-right, down, down-left, 
    # left, up-left, up, up-right
    directions = [
        (0, 1), (1, 1), (1, 0), (1, -1),
        (0, -1), (-1, -1), (-1, 0), (-1, 1)
    ]
    
    def check_word(row, col, dx, dy):
        # Check if "XMAS" starts at position (row, col) in direction (dx, dy)
        if not (0 <= row + 3*dx < rows and 0 <= col + 3*dy < cols):
            return False
        
        word = ''
        for i in range(4):  # XMAS is 4 letters
            word += grid[row + i*dx][col + i*dy]
        return word == 'XMAS'
    
    # Check every starting position and direction
    for i in range(rows):
        for j in range(cols):
            for dx, dy in directions:
                if check_word(i, j, dx, dy):
                    count += 1
    
    return count

def count_xmas_part2(grid):
    rows = len(grid)
    cols = len(grid[0])
    count = 0
    
    def check_x_pattern(row, col):
        # Need room for 3x3 pattern
        if not (0 <= row + 2 < rows and 0 <= col + 2 < cols):
            return False
        
        # Center must be 'A'
        if grid[row+1][col+1] != 'A':
            return False
            
        # Check all valid combinations for the diagonals
        # Each diagonal can be either MAS or SAM
        diagonals = [
            (grid[row][col] + grid[row+2][col+2]),     # top-left to bottom-right
            (grid[row][col+2] + grid[row+2][col])      # top-right to bottom-left
        ]
        
        valid_ends = {'MS', 'SM'}  # Valid combinations for diagonal ends
        
        return all(d[0] + d[1] in valid_ends for d in diagonals)
    
    # Check every possible center position of the X pattern
    for i in range(rows-2):
        for j in range(cols-2):
            if check_x_pattern(i, j):
                count += 1
    
    return count

def solve(filename):
    grid = read_input(filename)
    return count_xmas(grid)

if __name__ == "__main__":
    result = solve("input")
    print(f"Part 1: XMAS appears {result} times in the word search")
    
    result2 = count_xmas_part2(read_input("input"))
    print(f"Part 2: X-MAS appears {result2} times in the word search")