"""
Advent of Code 2025 - Day 3: Lobby
Solution for finding maximum joltage from battery banks.
"""
import time

# Expected answers for verification
EXPECTED_PART1 = 16858
EXPECTED_PART2 = 167549941654721


def digits_to_number(digits):
    """Convert a list of digits to an integer."""
    result = 0
    for digit in digits:
        result = result * 10 + digit
    return result


def remove_and_append(digits, position, new_digit):
    """Remove digit at position and append new_digit at the end."""
    return digits[:position] + digits[position + 1:] + [new_digit]


def would_improve_number(current_digits, position, new_digit, best_so_far):
    """Check if removing digit at position and appending new_digit improves the number."""
    new_digits = remove_and_append(current_digits, position, new_digit)
    return digits_to_number(new_digits) > best_so_far


def find_next_zero_index(digits):
    """Find the index of the first zero in the digits list."""
    for i, digit in enumerate(digits):
        if digit == 0:
            return i
    return -1


def find_best_two_digit_joltage(battery_line):
    """
    Find the maximum joltage from a battery bank using exactly 2 batteries.

    Strategy: Greedily maintain the two highest digits that maximize the value.
    """
    first = 0
    second = 0
    best_value = 0

    for char in battery_line:
        digit = int(char)

        # Fill initial positions
        if first == 0:
            first = digit
        elif second == 0:
            second = digit
        else:
            # Consider replacing second position with new digit
            if digit > second and (first * 10 + digit) > best_value:
                if second > first:
                    first = second
                second = digit
            # Consider replacing first position with current second and new digit
            elif second > first and (second * 10 + digit) > best_value:
                first = second
                second = digit

        # Update best value if both positions are filled
        if first != 0 and second != 0:
            best_value = first * 10 + second

    return best_value


def find_best_twelve_digit_joltage(battery_line):
    """
    Find the maximum joltage from a battery bank using exactly 12 batteries.

    Strategy: Fill 12 positions, then greedily replace digits to maximize value.
    """
    digits = [0] * 12
    best_value = 0

    for char in battery_line:
        digit = int(char)

        # Fill empty positions first
        zero_index = find_next_zero_index(digits)
        if zero_index != -1:
            digits[zero_index] = digit
        else:
            # Try removing each position and appending new digit to see if it improves
            for i in range(12):
                if would_improve_number(digits, i, digit, best_value):
                    digits = remove_and_append(digits, i, digit)
                    break

        # Update best value when all positions are filled
        if 0 not in digits:
            best_value = digits_to_number(digits)

    return best_value


def solve_part_one(input_file):
    """Solve part 1: Find total joltage using 2 batteries per bank."""
    total_joltage = 0

    with open(input_file, 'r') as file:
        for line in file:
            bank_joltage = find_best_two_digit_joltage(line.strip())
            total_joltage += bank_joltage

    return total_joltage


def solve_part_two(input_file):
    """Solve part 2: Find total joltage using 12 batteries per bank."""
    total_joltage = 0

    with open(input_file, 'r') as file:
        for line in file:
            bank_joltage = find_best_twelve_digit_joltage(line.strip())
            total_joltage += bank_joltage

    return total_joltage


def verify_answer(part, result, expected):
    """Verify that the computed answer matches the expected answer."""
    status = "✓" if result == expected else "✗"
    print(f"  Answer: {result} {status}")
    if result != expected:
        print(f"  Expected: {expected}")


def main():
    """Run both parts of the solution with timing."""
    print("=" * 60)
    print("Advent of Code 2025 - Day 3: Lobby")
    print("=" * 60)

    # Part 1
    print("\nPart 1: Maximum joltage with 2 batteries per bank")
    start_time = time.perf_counter()
    result_part1 = solve_part_one("input.txt")
    elapsed_time = time.perf_counter() - start_time
    print(f"  Time: {elapsed_time * 1000:.3f} ms")
    verify_answer(1, result_part1, EXPECTED_PART1)

    # Part 2
    print("\nPart 2: Maximum joltage with 12 batteries per bank")
    start_time = time.perf_counter()
    result_part2 = solve_part_two("input.txt")
    elapsed_time = time.perf_counter() - start_time
    print(f"  Time: {elapsed_time * 1000:.3f} ms")
    verify_answer(2, result_part2, EXPECTED_PART2)

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
