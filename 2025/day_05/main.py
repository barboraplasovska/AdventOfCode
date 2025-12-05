import time

def read_file(input_file):
    ranges = []
    ingredients = []
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue
            if "-" in line:
                low, high = line.split("-")
                ranges.append((int(low), int(high)))
            else:
                ingredients.append(int(line))

    ranges.sort()

    merged = []
    for range in ranges:
        merged = merge_ranges(merged, range[0], range[1])

    return merged, ingredients

def merge_ranges(ranges, x, y):
    replaced = False

    for i in range(0, len(ranges)):
        (a, b) = ranges[i]
        new_range = (-1, -1)

        if x < a:
            new_range = (x, max(y, b))
        elif x <= b:
            if y > b:
                new_range = (a, y)
            else:
                new_range = (a, b)

        if new_range != (-1, -1):
            ranges[i] = new_range
            replaced = True
            break

    if not replaced:
        ranges.append((x, y))
    return ranges

def part_one(ranges, ingredients):
    res = 0
    for ing in ingredients:
        for range in ranges:
            if range[0] <= ing <= range[1]:
                res += 1
                break

    return res

def part_two(ranges):
    res = 0
    for range in ranges:
        n = range[1] - range[0] + 1
        res += n
    return res

def run_test(input_file, expected_part1, expected_part2):
    print(f"\n{'='*60}")
    print(f"Testing: {input_file}")
    print(f"{'='*60}")

    ranges, ingredients = read_file(input_file)

    start = time.time()
    result_part1 = part_one(ranges, ingredients)
    time1 = (time.time() - start) * 1000

    start = time.time()
    result_part2 = part_two(ranges)
    time2 = (time.time() - start) * 1000

    status_p1 = "✓" if result_part1 == expected_part1 else "✗"
    status_p2 = "✓" if result_part2 == expected_part2 else "✗"

    print(f"Part 1: {result_part1:>15} (expected: {expected_part1:>15}) {status_p1} ({time1:.2f}ms)")
    print(f"Part 2: {result_part2:>15} (expected: {expected_part2:>15}) {status_p2} ({time2:.2f}ms)")

    return result_part1 == expected_part1 and result_part2 == expected_part2

def main():
    print("\n🎄 Advent of Code 2025 - Day 5 🎄")

    test_cases = [
        ("small_input.txt", 3, 14),
        ("input.txt", 513, 339668510830757),
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