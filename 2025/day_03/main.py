def sum_would_be_higher(a, b, sum):
    new_sum = a * 10 + b 
    return new_sum > sum

def find_highest_batteries(line):
    a = 0
    b = 0
    last_high = 0
    for letter in line:
        nb = int(letter)

        if a == 0:
            a = nb
        elif b == 0:
            b = nb
        else:
            if nb > b and sum_would_be_higher(a, nb, last_high):
                if b > a:
                    a = b 
                b = nb
            elif b > a and sum_would_be_higher(b, nb, last_high):
                a = b
                b = nb

        if a != 0 and b != 0:
            last_high = a * 10 + b
    return last_high

def part_one(input_file):
    res = 0
    with open(input_file, 'r') as file:
        for line in file:
            r = find_highest_batteries(line.strip())
            print(r)
            res += r
    return res

def calculate_sum(nbs):
    new_sum = 0
    mult = 1
    for nb in reversed(nbs):
        new_sum += nb * mult
        mult *= 10
    
    return new_sum

def nbs_without_i(nbs, i, nb):
    return nbs[:i] + nbs[i+1:] + [nb]

def sum_would_be_higher_without_i(nbs, i, nb, sum):
    copy_nbs = nbs_without_i(nbs, i, nb)
    new_sum = calculate_sum(copy_nbs)
    return new_sum > sum

def find_highest_batteries2(line):
    nbs = [ 0 ] * 12
    last_high = 0
    for letter in line:
        nb = int(letter)

        if any(x == 0 for x in nbs):
            i = 0
            while i < 12:
                if nbs[i] == 0:
                    nbs[i] = nb
                    break
                i += 1
        else:
            # I can add another number
            # if i drop one, will the number be higher ?
            i = 0
            while i < 12:
                if sum_would_be_higher_without_i(nbs, i, nb, last_high):
                    nbs = nbs_without_i(nbs, i, nb)
                    break
                i += 1

        if all(x != 0 for x in nbs):
            last_high = calculate_sum(nbs)
            
    return last_high

def part_two(input_file):
    res = 0
    with open(input_file, 'r') as file:
        for line in file:
            r = find_highest_batteries2(line.strip())
            res += r
    return res

def main():
    print(part_one("input.txt"))
    print(part_two("input.txt"))

main()