import re

def readFile(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    return lines

def is_symbol(c):
    return not c.isdigit() and c != '.'

def split_numbers(line):
    res = re.split(r'(\d+)', line)
    if line[0].isdigit():
        res.pop(0)
    if line[-1].isdigit():
        res.pop()
    return res

def part1(lines):
    numbers = []
    for i in range(len(lines)):
        j = 0
        while j < len(lines[i]):
            if lines[i][j].isdigit():
                start = j
                nb = ""
                while j < len(lines[i]) and lines[i][j].isdigit():
                    nb += lines[i][j]
                    j += 1
                j -= 1
                numbers.append((int(nb), (i, start, j)))
            j += 1

    sum = 0
    for nb in numbers:
        part_nbber = False
        for i in range(nb[1][0] - 1, nb[1][0] + 2):
            if i >= 0 and i < len(lines):
                for j in range(nb[1][1] - 1, nb[1][2] + 2):
                    if j >= 0 and j < len(lines[i]):
                        if not (lines[i][j].isdigit() or lines[i][j] == "."):
                            part_nbber = True
                            sum += nb[0]
                            break
                if part_nbber:
                    break

    return sum
                

def part2(lines):
    numbers = []
    for i in range(len(lines)):
        j = 0
        while j < len(lines[i]):
            if lines[i][j].isdigit():
                nb = ""
                start = j
                while j < len(lines[i]) and lines[i][j].isdigit():
                    nb += lines[i][j]
                    j += 1
                j -= 1
                numbers.append((int(nb), (i, start, j)))

            j += 1

    gears = {}
    for nb in numbers:
        for i in range(nb[1][0] - 1, nb[1][0] + 2):
            if i >= 0 and i < len(lines):
                for j in range(nb[1][1] - 1, nb[1][2] + 2):
                    if j >= 0 and j < len(lines[i]):
                        if lines[i][j] == "*":
                            if not gears.get((i, j)):
                                gears[(i, j)] = []
                            gears[(i, j)].append(nb[0])

    sum = 0
    for gear in gears:
        if len(gears[gear]) == 2:
            sum += gears[gear][0] * gears[gear][1]

    return sum

def main():
    lines = readFile("input.txt")
    print("part 1: " + str(part1(lines)))
    print("part 2: " + str(part2(lines)))

main()