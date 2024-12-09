
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

part2Blocks = blocks.copy()

print("PART2")
lastIndex = len(part2Blocks) - 1
fileList = []
freeSpaceList = []

freeSpaceIndex = 0
while (freeSpaceIndex < len(part2Blocks)):
    # Find start of free space
    while (freeSpaceIndex < len(part2Blocks)) and (part2Blocks[freeSpaceIndex] != '.'):
        freeSpaceIndex += 1
    startX = freeSpaceIndex
    while (freeSpaceIndex < len(part2Blocks)) and (part2Blocks[freeSpaceIndex] == '.'):
        freeSpaceIndex += 1

    if (startX < len(part2Blocks)):
        print(f"Free space found at {startX} length {freeSpaceIndex - startX}")
        freeSpaceList.append([startX, freeSpaceIndex - startX])

while (lastIndex > 0):
    fileStart = lastIndex
    while (lastIndex > 0):
        # Skip empty space
        if part2Blocks[lastIndex] in '.':
            lastIndex -= 1
            continue
        else:
            fileID = int(part2Blocks[lastIndex])
            fileSize = 0
            while int(part2Blocks[lastIndex]) == fileID:
                lastIndex -= 1
                fileSize += 1
                if (part2Blocks[lastIndex] == '.'):
                    break

            if (fileSize > 0):
                fileList.append([lastIndex + 1, fileID, fileSize, False])

fileList.sort(key=lambda x: (-x[1], -x[2]))

print(f"Part2 blocks {part2Blocks}")
print(f"Files {fileList}")
print(f"Free spaces {freeSpaceList}")

def findFreeSpace(b, startX):
    freeSize = 0
    while startX < len(b):
        if part2Blocks[startX] != '.':
            startX += 1
        else:
            break

    while startX < len(b) and b[startX] == '.':
        freeSize += 1
        startX += 1

    return startX, freeSize

def swapFileAndSpace(f, s):
   t = f[0]
   f[0] = s[0]
   s[0] = t

for f in fileList:
    print(f"FileID {f[1]} length {f[2]}")
    startX = 0

    for s in freeSpaceList:
        if s[0] < f[0] and s[1] >= f[2]:

            if (s[1] == f[2]):
                # swap the file with the free space of same size
                print(f"Swap file {f[1]} at {f[0]} length {f[2]} with space at {s[0]} length {s[1]}")
                swapFileAndSpace(s, f)
            else:
                # Create new free space at new location with matched length
                print(f"Created new space at {f[0]} length {f[2]}")
                freeSpaceList.append([f[0], f[2]])
                # Change existing free space to be shorter, at end of file
                print(f"Moved file {f[1]} to {s[0]}")
                f[0] = s[0]
                print(f"Changed free space at {s[0]} to be at {s[0] + f[2]} with length {s[1]-f[2]}") 
                s[0] = s[0] + f[2]
                s[1] = (s[1] - f[2])


#while True:
#    print(f"Scan blocks")
#    movedCount = 0
#    x = 0
#    lastBlock = len(part2Blocks) - 1

#        print(f"Free block of size {freeSize} found")
#        for f in fileList:
#            if not f[3] and (f[2] == freeSize) and x < f[0]:
#                print(f"Moved file {f[1]} of length {f[2]} from {f[0]} to {x-freeSize}")
#                part2Blocks = swapRange(part2Blocks, x - freeSize, f[0], f[2])
#                movedCount += 1
#                f[3] = True
#                break

#    if movedCount == 0:
#        break

fileList.sort(key=lambda x: (x[0]))
print(f"Files now {fileList}")

freeSpaceList.sort(key=lambda x: (x[0]))
print(f"Free space now {freeSpaceList}")

checksum = 0
for f in fileList:
    for i in range(0, f[2]):
        checksum += f[1] * (f[0]+i)

print(f"Checksum {checksum}")
