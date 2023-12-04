import re

def readFile(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    # remove useless "Game Id:"
    i = 0
    for i in range(len(lines)):
        lines[i] = lines[i].split(":")[1].replace("\n", "")
    return lines

limits = [[12, "red"], [13, "green"], [14, "blue"]]

def part1(lines):
    index = 1
    sum = 0
    for line in lines:
        sets = line.split(";")
        stop = False
        for set in sets:
            if stop:
                break
            cubes = set.split(",")
            for cube in cubes:
                if stop:
                    break
                cube = cube.strip()
                nb, color = cube.strip().split(" ")
                for limit in limits:
                    if color == limit[1]:
                        if int(nb) > limit[0]:
                            stop = True
                            break
        if not stop:
            sum += index
        index += 1
    return sum

def part2(lines):
    index = 1
    sum = 0
    for line in lines:
        sets = line.split(";")
        maxs = [0, 0, 0] # red, green, blue
        for set in sets:
            cubes = set.split(",")
            for cube in cubes:
                cube = cube.strip()
                nb, color = cube.strip().split(" ")
                if color == "red":
                    maxs[0] = max(maxs[0], int(nb))
                elif color == "green":
                    maxs[1] = max(maxs[1], int(nb))
                elif color == "blue":
                    maxs[2] = max(maxs[2], int(nb))
        sum += maxs[0] * maxs[1] * maxs[2]
        index += 1
    return sum

def main():
    lines = readFile("input.txt")
    print("part 1: " + str(part1(lines)))
    print("part 2: " + str(part2(lines)))
main()