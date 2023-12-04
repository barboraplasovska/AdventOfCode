def readFile(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].split(":")[1].strip().replace("\n", "")
    return lines

def part1(lines):
    res = 0
    for line in lines:
        winning, his = line.split("|")
        winning_nb = winning.strip().split(" ")
        his_nb = his.strip().split(" ")
        
        points = 0

        for nb in his_nb:
            if nb in winning_nb and nb != "":
                if points == 0:
                    points = 1
                else:
                    points *= 2
        res += points
    return res

def part2(lines):
    res = len(lines) * [1]
    for i in range(len(lines)):
        winning, his = lines[i].split("|")
        winning_nb = winning.strip().split(" ")
        his_nb = his.strip().split(" ")
        
        points = 0
        for nb in his_nb:
            if nb in winning_nb and nb != "":
                points += 1
        
        for j in range(res[i]):
            for k in range(i + 1, i + points + 1):
                res[k] += 1 

    sum = 0
    for i in res:
        sum += i
    return sum
        

def main():
    lines = readFile("input.txt")
    print("part 1: " + str(part1(lines)))
    print("part 2: " + str(part2(lines)))
main()