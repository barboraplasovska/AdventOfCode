import re

def readFile(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    return lines

def getTimeAndDistance(lines):
    time_line = lines[0].split(":")
    times = time_line[1].strip().split(" ")
    while "" in times:
        times.remove("")
    distance_line = lines[1].split(":")
    distances = distance_line[1].strip().split(" ")
    while "" in distances:
        distances.remove("")
    times = [int(x) for x in times]
    distances = [int(x) for x in distances]
    print(times)
    return times, distances

def part1(lines):
    times, distances = getTimeAndDistance(lines)
    res = [0] * len(times)
    for i in range(len(times)):
        for j in range(times[i]):
            acc = j * 1
            dist = (times[i] - j) * acc
            if dist > distances[i]:
                res[i] += 1
    
    result = 1
    for i in range(len(res)):
        result *= res[i]
    return result

def getTimeAndDistance2(lines):
    for i in range(len(lines)):
        lines[i] = lines[i].split(":")[1].replace(" ", "")
    
    time = int(lines[0])
    distance = int(lines[1])

    return time, distance
               

def part2(lines):
    time, distance = getTimeAndDistance2(lines)
    res = 0
    for j in range(time):
        acc = j * 1
        dist = (time - j) * acc
        if dist > distance:
            res += 1
    return res

def main():
    lines = readFile("input.txt")
    print("part 1: " + str(part1(lines)))
    print("part 2: " + str(part2(lines)))
main()