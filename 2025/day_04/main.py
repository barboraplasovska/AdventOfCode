def read_file(input_file):
    M = []
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            arr = [0 if x == '.' else 1 for x in line]
            M.append(arr)
    return M 

def get_coordinates(M, a, b, x, y):
    coords = []
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1),
    ]

    for da, db in directions:
        na, nb = a + da, b + db
        if 0 <= na < x and 0 <= nb < y:
            coords.append(M[na][nb])
    
    return coords

def count_rolls(coords):
    return coords.count(1) + coords.count(3)

def print_pretty(M):
    for i in range(0, len(M)):
        for j in range(0, len(M[0])):
            c = M[i][j]
            if c == 0:
                print(".", end="")
            elif c == 1:
                print("@", end="")
            else:
                print("x", end="")
        print("")

def mark_removed_rolls(M, x, y):
     for i in range(0, x):
        for j in range(0, y):
            if M[i][j] == 3:
                M[i][j] = 0

def part_one(M, x, y):
    res = 0

    for i in range(0, x):
        for j in range(0, y):
            if M[i][j] == 1 or M[i][j] == 3:
                coords = get_coordinates(M, i, j, x, y)
                rolls = count_rolls(coords)
                if rolls < 4:
                    M[i][j] = 3
                    res += 1
    return res

def part_two(M,  x, y):
    res = 0
    made_change = True

    while made_change:
        removed = part_one(M,  x, y)
        res += removed
        mark_removed_rolls(M, x, y)
        made_change = removed > 0
    
    return res


def run_test(input_file, expected_part1, expected_part2):
    print(f"\n{'='*60}")
    print(f"Testing: {input_file}")
    print(f"{'='*60}")

    # Part 1
    M = read_file(input_file)
    x, y = len(M), len(M[0])
    result_part1 = part_one(M, x, y)

    # Need to reload for part 2 since part 1 modifies the matrix
    M = read_file(input_file)
    result_part2 = part_two(M, x, y)

    # Display results
    status_p1 = "✓" if result_part1 == expected_part1 else "✗"
    status_p2 = "✓" if result_part2 == expected_part2 else "✗"

    print(f"Part 1: {result_part1:>6} (expected: {expected_part1:>6}) {status_p1}")
    print(f"Part 2: {result_part2:>6} (expected: {expected_part2:>6}) {status_p2}")

    return result_part1 == expected_part1 and result_part2 == expected_part2


def main():
    print("\n🎄 Advent of Code 2025 - Day 4 🎄")

    # Test cases with expected answers
    test_cases = [
        ("small_input.txt", 13, 43),
        ("input.txt", 1437, 8765),
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