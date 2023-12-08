import math

def readFile(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()


    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    return lines

def part1(lines):
    instructions = lines[0]
    roots = []
    left = []
    right = []

    for i in range(2, len(lines)):
        lines[i] = lines[i].replace("= (", "").replace(")", "").replace(",", "")
        ll = lines[i].split()
        if ll[0] not in roots:
            roots.append(ll[0])
        left.append(ll[1])
        right.append(ll[2])

    count = 0
    i = 0
    node = roots.index("AAA")
    curr = "AAA"
    while curr != "ZZZ":
        if instructions[i] == "L":
            curr = left[node]
            node = roots.index(curr)
        else:
            curr = right[node]
            node = roots.index(curr)
        i += 1
        if i >= len(instructions):
            i = 0
        count += 1
    
    return count
   
def findNodesWithA(roots):
    res = []
    for i in range(len(roots)):
        if roots[i][2] == "A":
            res.append(i)
    return res

def moveLeft(roots, nodes, left):
    for i in range(len(nodes)):
        nodes[i] = roots.index(left[nodes[i]])
    return nodes

def moveRight(roots, nodes, right):
    for i in range(len(nodes)):
        nodes[i] = roots.index(right[nodes[i]])
    return nodes

def part2(lines):
    instructions = lines[0]
    roots = []
    left = []
    right = []

    for i in range(2, len(lines)):
        lines[i] = lines[i].replace("= (", "").replace(")", "").replace(",", "")
        ll = lines[i].split()
        if ll[0] not in roots:
            roots.append(ll[0])
        left.append(ll[1])
        right.append(ll[2])

    curr = findNodesWithA(roots)
    count = 0
    ind = 0

    least_count = [0] * len(curr)
    
    while 0 in least_count:
        for i, node_i in enumerate(curr):
            node = roots[node_i]
            if node.endswith("Z") and least_count[i] == 0:
                least_count[i] = count
        
        if instructions[ind] == "L":
            curr = moveLeft(roots, curr, left)
        else:
            curr = moveRight(roots, curr, right)
        ind = (ind + 1) % len(instructions)
        count += 1

    return math.lcm(*least_count)

def main():
    lines = readFile("input.txt")
    print("part 1: " + str(part1(lines)))
    print("part 2: " + str(part2(lines)))
main()