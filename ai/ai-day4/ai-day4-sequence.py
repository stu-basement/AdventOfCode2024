def read_input(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip().isalpha() and line.strip().isupper()]

def find_xmas_patterns(grid):
    width = len(grid[0])
    sequence = ''.join(grid)
    count = 0
    
    for i, char in enumerate(sequence):
        if char != 'A':
            continue
            
        # Calculate row position to check for wrapping
        current_row = i // width
        
        # Skip if too close to top/bottom
        if i < width or i >= len(sequence) - width:
            continue
            
        tl = i - (width + 1)  # top-left
        tr = i - (width - 1)  # top-right
        bl = i + (width - 1)  # bottom-left
        br = i + (width + 1)  # bottom-right
        
        # Check if we have valid positions and no wrapping
        if (tl < 0 or br >= len(sequence) or 
            tl // width != (current_row - 1) or  # top positions must be in row above
            br // width != (current_row + 1) or  # bottom positions must be in row below
            tr // width != (current_row - 1) or
            bl // width != (current_row + 1)):
            continue
            
        # Check all valid diagonal combinations
        tl_br = sequence[tl] + sequence[br]  # top-left to bottom-right
        tr_bl = sequence[tr] + sequence[bl]  # top-right to bottom-left
        
        # Valid combinations are MS or SM
        valid_diagonals = {'MS', 'SM'}
        if tl_br in valid_diagonals and tr_bl in valid_diagonals:
            count += 1
            
    return count

def solve_part2(filename):
    grid = read_input(filename)
    return find_xmas_patterns(grid)

if __name__ == "__main__":
    result = solve_part2("input")
    print(f"Part 2: X-MAS appears {result} times in the word search") 