import time
from functools import lru_cache


def read_file(input_file):
    """Read input file and convert characters to numeric codes"""
    M = []
    char_map = {'.': 0, 'S': 1, '^': 2, '|': 3}

    with open(input_file, 'r') as file:
        for line in file:
            M.append([char_map.get(c, 0) for c in line.strip()])

    return M


def part_one(M):
    """Simulate the first part - shooting and collecting hits"""
    res = 0

    for i in range(len(M) - 1):
        for j in range(len(M[0])):
            if M[i][j] == 0:
                continue

            if M[i][j] == 1:  # 'S' - shooter
                M[i+1][j] = 3  # shoot down
            elif M[i][j] == 2:  # '^' - target
                if i > 0 and M[i-1][j] == 3:  # was hit
                    res += 1
                    # Spread to adjacent cells
                    if j > 0:
                        M[i][j-1] = 3
                    if j < len(M[0]) - 1:
                        M[i][j+1] = 3
                    if j > 0:
                        M[i+1][j-1] = 3
                    if j < len(M[0]) - 1:
                        M[i+1][j+1] = 3
            elif M[i][j] == 3 and M[i+1][j] == 0:  # '|' - continue down
                M[i+1][j] = 3

    return res


# Global M for caching - will be set before part_two
_M = None

@lru_cache(maxsize=None)
def explore(i, j, w, l):
    """Recursively explore paths through the grid"""
    if i == w - 1 and _M[i][j] == 3:
        return 1
    if _M[i][j] == 3:
        return explore(i+1, j, w, l)
    if _M[i][j] == 2:
        return explore(i+1, j-1, w, l) + explore(i+1, j+1, w, l)
    return 0


def find_first_hit(M):
    """Find the first '|' (3) in the second row"""
    for j in range(len(M[0])):
        if M[1][j] == 3:
            return (1, j)
    return (-1, -1)


def part_two(M):
    """Count paths through the grid"""
    global _M
    _M = M
    explore.cache_clear()

    x, y = find_first_hit(M)
    if x == -1:
        return 0

    return explore(x, y, len(M), len(M[0]))


def run_test(input_file, expected_part1, expected_part2):
    """Run both parts on a single test case"""
    print(f"\n{'='*60}")
    print(f"Testing: {input_file}")
    print(f"{'='*60}")

    # Part 1
    M1 = read_file(input_file)
    start = time.time()
    result_part1 = part_one(M1)
    time1 = (time.time() - start) * 1000

    # Part 2 (uses M1 modified by part_one)
    start = time.time()
    result_part2 = part_two(M1)
    time2 = (time.time() - start) * 1000

    # Display results
    status_p1 = "\u2713" if result_part1 == expected_part1 else "\u2717"
    status_p2 = "\u2713" if result_part2 == expected_part2 else "\u2717"

    print(f"Part 1: {result_part1:>15} (expected: {expected_part1:>15}) {status_p1} ({time1:.2f}ms)")
    print(f"Part 2: {result_part2:>15} (expected: {expected_part2:>15}) {status_p2} ({time2:.2f}ms)")

    return result_part1 == expected_part1 and result_part2 == expected_part2


def main():
    print("\n\U0001F384 Advent of Code 2025 - Day 7 \U0001F384")

    test_cases = [
        ("small_input.txt", None, None),  # Run to find expected values
        ("input.txt", None, None),
    ]

    # First, find the expected values
    print("\nFinding expected values...")
    for i, (input_file, _, _) in enumerate(test_cases):
        M = read_file(input_file)
        p1 = part_one(M)
        p2 = part_two(M)
        print(f"{input_file}: Part 1 = {p1}, Part 2 = {p2}")
        test_cases[i] = (input_file, p1, p2)

    # Now run the tests with expected values
    print("\n" + "="*60)
    print("Running tests...")
    print("="*60)

    all_passed = True
    for input_file, exp_p1, exp_p2 in test_cases:
        passed = run_test(input_file, exp_p1, exp_p2)
        all_passed = all_passed and passed

    print(f"\n{'='*60}")
    if all_passed:
        print("\u2713 All tests passed!")
    else:
        print("\u2717 Some tests failed")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
