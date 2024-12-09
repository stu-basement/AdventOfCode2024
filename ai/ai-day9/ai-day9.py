def parse_disk_map(disk_map):
    # Convert string of numbers into list of alternating file/space lengths
    lengths = [int(x) for x in disk_map]
    
    # Convert to blocks representation with file IDs
    blocks = []
    file_id = 0
    
    for i, length in enumerate(lengths):
        if i % 2 == 0:  # File blocks
            blocks.extend([file_id] * length)
            file_id += 1
        else:  # Free space blocks
            blocks.extend([-1] * length)  # -1 represents free space
            
    return blocks

def compact_blocks_part1(blocks):
    """Move blocks one at a time from right to left"""
    result = blocks.copy()
    
    for i in range(len(result)):
        if result[i] == -1:  # Found a free space
            # Look for rightmost file block
            for j in range(len(result)-1, i, -1):
                if result[j] != -1:  # Found a file block
                    # Move the block
                    result[i] = result[j]
                    result[j] = -1
                    break
    return result

def compact_blocks_part2(blocks):
    """Move whole files from right to left"""
    result = blocks.copy()
    
    # Get highest file ID
    max_file_id = max(x for x in result if x != -1)
    
    # Process files in decreasing order of file ID
    for file_id in range(max_file_id, -1, -1):
        # Find file size and position
        file_positions = [i for i, x in enumerate(result) if x == file_id]
        if not file_positions:
            continue
            
        file_size = len(file_positions)
        file_start = min(file_positions)
        
        # Look for leftmost viable free space
        current_space = 0
        space_start = -1
        
        for i in range(file_start):
            if result[i] == -1:
                if space_start == -1:
                    space_start = i
                current_space += 1
                if current_space == file_size:
                    # Move the entire file
                    for j in range(file_size):
                        result[space_start + j] = file_id
                        result[file_positions[j]] = -1
                    break
            else:
                current_space = 0
                space_start = -1
                
    return result

def calculate_checksum(blocks):
    return sum(pos * block_id 
              for pos, block_id in enumerate(blocks) 
              if block_id != -1)

def solve_day9(input_data):
    # Parse input
    blocks = parse_disk_map(input_data)
    
    # Part 1
    compact_result1 = compact_blocks_part1(blocks)
    checksum1 = calculate_checksum(compact_result1)
    
    # Part 2
    compact_result2 = compact_blocks_part2(blocks)
    checksum2 = calculate_checksum(compact_result2)
    
    return checksum1, checksum2

def main():
    # Read input from file
    try:
        with open('input', 'r') as f:
            puzzle_input = f.read().strip()
    except FileNotFoundError:
        print("Error: 'input' file not found")
        return
    except Exception as e:
        print(f"Error reading input file: {e}")
        return

    # Solve both parts
    try:
        part1, part2 = solve_day9(puzzle_input)
        print(f"Part 1 Checksum: {part1}")
        print(f"Part 2 Checksum: {part2}")
    except Exception as e:
        print(f"Error solving puzzle: {e}")

if __name__ == "__main__":
    main() 