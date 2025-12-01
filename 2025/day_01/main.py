# part 1

def handle_number1(nb, line):
    direction = line[0]
    distance = int(line[1:])

    while distance > 100:
        distance -= 100

    if direction == "L":
        if nb - distance < 0:
            nb = 100 + (nb - distance)
        else:
            nb -= distance
    else:
        if nb + distance > 99:
            nb = nb + distance - 100
        else:
            nb += distance
    
    return nb

def part_one(input_file):
    nb = 50
    res = 0

    with open(input_file, 'r') as file:
       for line in file:
            nb = handle_number1(nb, line)
            if nb == 0:
                res += 1

    return res

# part 2

def handle_number2(nb, line):
    direction = line[0]
    distance = int(line[1:])
    click = 0

    start = nb

    while distance > 100:
        distance -= 100
        click += 1

    if direction == 'L':
        if nb - distance < 0:
            nb = 100 + (nb - distance)
            if start != 0 and nb != 0:
                click += 1
        else:
            nb -= distance
    else:
        if nb + distance > 99:
            nb = nb + distance - 100
            if start != 0 and nb != 0:
                click += 1
        else:
            nb += distance

    return (nb, click)

def part_two(input_file):
    nb = 50
    res = 0

    with open(input_file, 'r') as file:
       for line in file:
            (nb, click) = handle_number2(nb, line)
            if nb == 0:
                res += 1
            res += click

    return res

def main():
    input_file = "input.txt"

    res1 = part_one(input_file)
    res2 = part_two(input_file)

    print("part 1: ", res1)
    print("part 2: ", res2)

main()
