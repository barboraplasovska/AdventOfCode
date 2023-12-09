import numpy as np

def readFile(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    return lines

def get_next(nbs):
    diffs, last_nbs = nbs, [nbs[-1]]
    while sum(abs(df) for df in diffs) > 0:
        diffs = [ diffs[i+1] - diffs[i] for i in range(len(diffs) - 1) ]
        last_nbs.append(diffs[-1])
    return sum(last_nbs)

def part1(lines):
    sum = 0
    for line in lines:
        nb = [int(x) for x in line.split(' ')]
        sum += get_next(nb)
    return sum

def part2(lines):
    sum = 0
    for line in lines:
        nb = [int(x) for x in line.split(' ')]
        sum += get_next(list(reversed(nb)))
    return sum

def main():
    lines = readFile("input.txt")
    print("part 1: " + str(part1(lines)))
    print("part 2: " + str(part2(lines)))
main()