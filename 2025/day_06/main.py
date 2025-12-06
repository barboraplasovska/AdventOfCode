import time


def read_file_part1(input_file):
    """Parse input file for part 1: numbers and operators in columns."""
    nbs = []
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            line_nb = line.split()
            if line_nb[0].isdigit():
                nbs.append([int(x) for x in line_nb])
            else:
                nbs.append(line_nb)
    return nbs


def part_one(nbs):
    """Calculate result by applying operations column-wise."""
    res = 0
    for i in range(len(nbs[0])):
        op = nbs[-1][i]
        temp = nbs[0][i]
        for j in range(1, len(nbs) - 1):
            if op == '+':
                temp += nbs[j][i]
            else:
                temp *= nbs[j][i]
        res += temp
    return res


def read_file_part2(input_file):
    """Read input file as raw lines for part 2."""
    with open(input_file, 'r') as file:
        return [line for line in file]


def separate_numbers(M):
    """Separate numbers in each line based on column spacing."""
    spaces = []
    temp = 0
    for i in range(1, len(M[-1])):
        if M[-1][i] == " ":
            temp += 1
            continue
        spaces.append(temp)
        temp = 0
    spaces.append(temp)

    res = []
    for j in range(len(M)):
        nbs = []
        ind = 0
        temp = 0
        start = 0
        for i in range(len(M[j]) - 1):
            if temp <= spaces[ind]:
                temp += 1
            else:
                nb = M[j][start:i]
                nbs.append(nb)
                start = i
                temp = 1
                ind += 1
        nbs.append(M[j][start:len(M[j]) - 1])
        res.append(nbs)

    transpose = list(map(list, zip(*res)))
    return transpose


def find_new_numbers(M):
    """Extract numbers by reading columns in reverse."""
    res = []
    for k in range(len(M)):
        arr = M[k]
        temp = []
        for j in range(len(arr[0]) - 1, -1, -1):
            t = ""
            for i in range(len(arr) - 1):
                t += arr[i][j]
            temp.append(t)
        res.append([x.strip() for x in temp])

    M = [[int(x) for x in row if x != ""] for row in res]
    return M


def get_operands(nbs):
    """Extract operators from each column."""
    return [row[-1].strip() for row in nbs]


def part_two(nbs):
    """Calculate result with complex number parsing and operations."""
    separated = separate_numbers(nbs)
    operands = get_operands(separated)
    numbers = find_new_numbers(separated)

    res = 0
    for i in range(len(operands)):
        temp = numbers[i][0]
        for j in range(1, len(numbers[i])):
            if operands[i] == '*':
                temp *= numbers[i][j]
            else:
                temp += numbers[i][j]
        res += temp
    return res


def run_test(input_file, expected_part1, expected_part2):
    print(f"\n{'='*60}")
    print(f"Testing: {input_file}")
    print(f"{'='*60}")

    nbs_part1 = read_file_part1(input_file)
    nbs_part2 = read_file_part2(input_file)

    start = time.time()
    result_part1 = part_one(nbs_part1)
    time1 = (time.time() - start) * 1000

    start = time.time()
    result_part2 = part_two(nbs_part2)
    time2 = (time.time() - start) * 1000

    status_p1 = "✓" if result_part1 == expected_part1 else "✗"
    status_p2 = "✓" if result_part2 == expected_part2 else "✗"

    print(f"Part 1: {result_part1:>15} (expected: {expected_part1:>15}) {status_p1} ({time1:.2f}ms)")
    print(f"Part 2: {result_part2:>15} (expected: {expected_part2:>15}) {status_p2} ({time2:.2f}ms)")

    return result_part1 == expected_part1 and result_part2 == expected_part2


def main():
    print("\n🎄 Advent of Code 2025 - Day 6 🎄")

    test_cases = [
        ("small_input.txt", 4277556, 3263827),
        ("input.txt", 5060053676136, 9695042567249),
    ]

    all_passed = True
    for input_file, exp_p1, exp_p2 in test_cases:
        passed = run_test(input_file, exp_p1, exp_p2)
        all_passed = all_passed and passed

    print(f"\n{'='*60}")
    if all_passed:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()