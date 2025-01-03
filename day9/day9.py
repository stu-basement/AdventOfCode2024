""" AdventOfCode Day 9 """
# PART 1
with open("input", "r", encoding="utf8") as f:
    disk_map = list(map(int, f.read().strip()))

# slice the disk map into blocks and spaces
blocks = disk_map[slice(0, len(disk_map), 2)]
spaces = disk_map[slice(1, len(disk_map), 2)]

expanded = []
i=0
for j, block in enumerate(blocks):
    for _ in range(block):
        expanded.append(i)
    i+=1
    if j<len(spaces):
        for _ in range(spaces[j]):
            expanded.append(-1)

block_index = len(expanded) - 1
space_index = 0
while space_index < block_index:
    while expanded[space_index] != -1 and space_index < block_index:
        space_index += 1

    expanded[space_index], expanded[block_index] = expanded[block_index], expanded[space_index]
    block_index -= 1

checksum = 0
for n, file_id in enumerate(expanded):
    if file_id != -1:
        checksum += (n * file_id)
print(f"PART1 Checksum: {checksum}")

files = []
spaces = []
position = 0
for block, block_len in enumerate(disk_map):
    if block % 2 == 0:
        # this is a file of length block_len
        files.append( (position, block_len) )
    elif block_len:
        # this is a space of length block_len
        spaces.append( (position, block_len) )
    position += block_len

file_id = len(files) - 1
while file_id >= 0:
    file_position, file_len = files[file_id]
    for space_index, (space_position, space_len) in enumerate(spaces):
        if space_position >= file_position:
            break

        if space_len >= file_len:
            # move the file into the space, shorten the space as necessary
            files[file_id] = (space_position, file_len)
            spaces[space_index] = (space_position + file_len, space_len - file_len)
            break

    file_id -= 1

checksum = 0
for file_id, (file_position, file_len) in enumerate(files):
    for p in range(file_len):
        checksum += file_id * (file_position + p)

print(f"PART2 Checksum: {checksum}")
