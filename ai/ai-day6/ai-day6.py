def read_input(filename):
    with open(filename) as f:
        return [list(line.strip()) for line in f if line.strip()]

class Guard:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        # direction: 0=up, 1=right, 2=down, 3=left
        self.direction = direction
        
    def turn_right(self):
        self.direction = (self.direction + 1) % 4
        
    def get_next_position(self):
        if self.direction == 0:  # up
            return self.x, self.y - 1
        elif self.direction == 1:  # right
            return self.x + 1, self.y
        elif self.direction == 2:  # down
            return self.x, self.y + 1
        else:  # left
            return self.x - 1, self.y

def find_guard_start(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] in '^>v<':
                direction = {'^': 0, '>': 1, 'v': 2, '<': 3}[grid[y][x]]
                return Guard(x, y, direction)
    return None

def is_valid_position(x, y, grid):
    return (0 <= y < len(grid) and 
            0 <= x < len(grid[0]))

def simulate_guard_path(grid, detect_loops=False):
    guard = find_guard_start(grid)
    visited_positions = set()
    visited_states = set()
    max_steps = 10000
    steps = 0
    
    while guard is not None and steps < max_steps:
        current_state = (guard.x, guard.y, guard.direction)
        visited_positions.add((guard.x, guard.y))
        
        if detect_loops and current_state in visited_states:
            return (True, len(visited_positions))
            
        visited_states.add(current_state)
        steps += 1
        
        # Get next position
        next_x, next_y = guard.get_next_position()
        
        # Check if next position is valid and not blocked
        if not is_valid_position(next_x, next_y, grid):
            return (False, len(visited_positions)) if detect_loops else len(visited_positions)
            
        if grid[next_y][next_x] in '#O':
            # Obstacle ahead, turn right
            guard.turn_right()
        else:
            # Move forward
            guard.x, guard.y = next_x, next_y
            
    return (False, len(visited_positions)) if detect_loops else len(visited_positions)

def solve_part1(filename):
    grid = read_input(filename)
    return simulate_guard_path(grid)

def solve_part2(filename):
    grid = read_input(filename)
    guard_start = find_guard_start(grid)
    loop_positions = 0
    
    # Try each empty position
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '.' and (x != guard_start.x or y != guard_start.y):
                # Try placing obstruction here
                test_grid = [row[:] for row in grid]
                test_grid[y][x] = 'O'
                
                # Check if this creates a loop
                is_loop, _ = simulate_guard_path(test_grid, detect_loops=True)
                if is_loop:
                    loop_positions += 1
    
    return loop_positions

if __name__ == "__main__":
    result1 = solve_part1("input")
    print(f"Part 1: The guard visits {result1} distinct positions")
    
    result2 = solve_part2("input")
    print(f"Part 2: There are {result2} positions that create loops")