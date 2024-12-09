
def swapBlocks(b, x, x1):
    if b[x] == '.':
        t = b[x]
        b[x] = b[x1]
        b[x1] = t
    return b

def swapRange(b, x, x1, n):
    for i in range(0, n):
        b = swapBlocks(b, x+i, x1+i)
    return b

# PART 1
with open("input", "r") as f:
     diskMap = list(f.read())

print(f"Start with {diskMap}")
mapIndex = 0
blocks = []
fileID = 0
while mapIndex < len(diskMap) - 1:
    fileLen = diskMap[mapIndex]
    mapIndex += 1
    for i in range(0, int(fileLen)):
        blocks.append(str(fileID))

    if diskMap[mapIndex] != '\n':
        freeSpaceLen = diskMap[mapIndex]
        mapIndex += 1

        for i in range(0, int(freeSpaceLen)):
            blocks.append('.')

    fileID += 1

print(f"Blocks: {blocks}")

print(f"{len(blocks)} in blocks")
for x in range(0, len(blocks)):
    print(f"Block {x} of {len(blocks)}")
    if blocks[x] == '.':
        for lastBlock in range(len(blocks) - 1, x+1, -1):
            if blocks[lastBlock] != '.' and lastBlock > x: 
                blocks = swapBlocks(blocks, x, lastBlock)

print(f"Packed {blocks}")

mapIndex = 0
checksum = 0
while mapIndex < len(blocks):
    if blocks[mapIndex] != '.':
        fileID = blocks[mapIndex]

        if blocks[mapIndex] != '0' and blocks[mapIndex] == fileID:
            checksum += (mapIndex * int(fileID))
               
    mapIndex += 1

print(f"Checksum {checksum}")
