def calculate_total_distance(filename):
    # Read the pairs directly from the input file
    left_list = []
    right_list = []
    
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # Skip empty lines
                left, right = map(int, line.split())
                left_list.append(left)
                right_list.append(right)
    
    # Sort both lists
    left_list.sort()
    right_list.sort()
    
    # Calculate total distance
    total_distance = sum(abs(a - b) for a, b in zip(left_list, right_list))
    
    return total_distance

def calculate_similarity_score(filename):
    # Read the pairs directly from the input file
    left_list = []
    right_list = []
    
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # Skip empty lines
                left, right = map(int, line.split())
                left_list.append(left)
                right_list.append(right)
    
    # Calculate similarity score
    total_score = 0
    for num in left_list:
        count = right_list.count(num)
        total_score += num * count
    
    return total_score

# Part 1: Calculate and print the distance
result = calculate_total_distance('input')
print(f"Part 1 - The total distance between the lists is: {result}")

# Part 2: Calculate and print the similarity score
result = calculate_similarity_score('input')
print(f"Part 2 - The similarity score is: {result}")
