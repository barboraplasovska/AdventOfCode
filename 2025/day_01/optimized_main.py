# part 1

def handle_number1(nb, line):
    direction = line[0]
    distance = int(line[1:])
    
    if direction == 'R':
        delta = distance
    else:
        delta = -distance
    
    return (nb + delta) % 100

def part_one(input_file):
    nb = 50
    zero_count = 0

    with open(input_file, 'r') as file:
        for line in file:
            nb = handle_number1(nb, line.strip())
            if nb == 0:
                zero_count += 1

    return zero_count

# part 2

def handle_number2(nb, line):
    direction = line[0]
    distance = int(line[1:])
    
    start = nb
    
    # Count full circles (every 100 clicks passes through 0 once)
    zero_crossings = distance // 100
    
    nb = handle_number1(nb, line)
    
    # Check if we crossed 0 during the partial rotation
    if start != 0 and nb != 0:
        if direction == 'R':
            if nb < start:
                zero_crossings += 1
        else:
            if nb > start:
                zero_crossings += 1
    
    return (nb, zero_crossings)

def part_two(input_file):
    nb = 50
    zero_count = 0

    with open(input_file, 'r') as file:
        for line in file:
            (nb, zero_crossings) = handle_number2(nb, line.strip())
            if nb == 0:
                zero_count += 1
            zero_count += zero_crossings

    return zero_count

def main():
    input_file = "input.txt"

    res1 = part_one(input_file)
    res2 = part_two(input_file)

    print("part 1: ", res1, "1074")
    print("part 2: ", res2, "6254")

main()
