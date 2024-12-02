def is_safe_report(levels):
    if len(levels) < 2:
        return False
    
    # Check first two numbers to determine if we're looking for increasing or decreasing
    is_increasing = levels[1] > levels[0]
    
    # Check each adjacent pair
    for i in range(len(levels) - 1):
        diff = levels[i + 1] - levels[i]
        
        # If increasing, diff should be positive 1-3
        # If decreasing, diff should be negative -1 to -3
        if is_increasing:
            if diff <= 0 or diff > 3:
                return False
        else:
            if diff >= 0 or diff < -3:
                return False
    
    return True

def is_safe_with_dampener(levels):
    # First check if it's safe without removing any numbers
    if is_safe_report(levels):
        return True
    
    # Try removing each number one at a time
    for i in range(len(levels)):
        # Create new list without the current number
        dampened_levels = levels[:i] + levels[i+1:]
        if is_safe_report(dampened_levels):
            return True
    
    return False

def count_safe_reports(filename, use_dampener=False):
    safe_count = 0
    
    with open(filename, 'r') as file:
        for line in file:
            # Skip empty lines and lines without numbers
            if not line.strip() or not any(c.isdigit() for c in line):
                continue
            
            # Parse the levels
            levels = [int(x) for x in line.split()]
            
            # Check if safe (with or without dampener)
            if use_dampener:
                if is_safe_with_dampener(levels):
                    safe_count += 1
            else:
                if is_safe_report(levels):
                    safe_count += 1
    
    return safe_count

# Part 1: Calculate and print the result without dampener
result = count_safe_reports('input')
print(f"Part 1 - The number of safe reports is: {result}")

# Part 2: Calculate and print the result with dampener
result = count_safe_reports('input', use_dampener=True)
print(f"Part 2 - The number of safe reports with dampener is: {result}") 