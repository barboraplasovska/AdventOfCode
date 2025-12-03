"""
Advent of Code 2025 - Day 2: Gift Shop Invalid IDs

This solution finds "invalid" product IDs in given ranges:
- Part 1: IDs where the number is split in half and both halves are identical (e.g., 1212, 333333)
- Part 2: IDs with any repeating pattern (e.g., 11, 123123, 12341234)

The optimized version uses "jumping" to skip to the next candidate rather than checking every number.
"""

import time


def parse_input(filepath):
    """Read and parse the input file into a list of (start, end) tuples."""
    with open(filepath, "r", encoding="utf-8") as f:
        ranges_str = f.read().strip().split(",")

    ranges = []
    for range_str in ranges_str:
        start, end = range_str.split("-")
        ranges.append((start, end))
    return ranges


# ============================================================================
# Pattern Detection Functions
# ============================================================================

def has_half_repeat(num_str):
    """Check if a number string is made of two identical halves.

    Examples: '1212' -> True, '333333' -> True, '123' -> False, '1234' -> False
    """
    length = len(num_str)
    if length % 2 != 0:
        return False

    mid = length // 2
    return num_str[:mid] == num_str[mid:]


def get_divisors(n):
    """Get all proper divisors of n (excluding n itself) in descending order."""
    divisors = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)

    # Remove n itself and sort in descending order
    return sorted([d for d in divisors if d != n], reverse=True)


def has_repeating_pattern(num_str):
    """Check if a number string is made of any repeating pattern.

    Examples: '11' -> True, '123123' -> True, '1234' -> False
    """
    length = len(num_str)

    if length == 1:
        return False

    # Quick check: all same digit (most common case)
    if len(set(num_str)) == 1:
        return True

    # Check each possible pattern length (must be a divisor of total length)
    for pattern_len in get_divisors(length):
        pattern = num_str[:pattern_len]
        if pattern * (length // pattern_len) == num_str:
            return True

    return False


# ============================================================================
# Part 1: Half-Repeat Pattern (e.g., 1212, 333333)
# ============================================================================

def jump_to_next_half_repeat_candidate(current_str):
    """Given a number string that is NOT a half-repeat, find the next potential one."""
    length = len(current_str)
    half = length // 2

    # If odd length, jump to next even length pattern
    if length % 2 == 1:
        # Next even-length pattern starts at 10^half repeated twice
        # e.g., from 123 (odd) -> 1010
        return str(10 ** half) * 2

    # Even length: construct half-repeat pattern
    first_half = int(current_str[:half])
    second_half = int(current_str[half:])

    # If first half is less than second half, increment it
    if first_half < second_half:
        first_half += 1

    # Create the candidate
    candidate = f"{first_half}{first_half}"

    # Check if we've gone past what this length can hold (all 9s case)
    if len(candidate) > length:
        # Jump to next length pattern
        return str(10 ** half) * 2

    return candidate


def sum_half_repeat_patterns(ranges):
    """Find and sum all numbers in ranges that have half-repeat patterns.

    Uses an optimization: instead of checking every number, we jump to the next
    potential half-repeat candidate.
    """
    total = 0

    for start_str, end_str in ranges:
        end_int = int(end_str)
        current = start_str

        while int(current) <= end_int:
            if has_half_repeat(current):
                total += int(current)
                # Jump past this pattern (increment by 10^half + 1)
                half = len(current) // 2
                step = 10 ** half + 1
                current = str(int(current) + step)
            else:
                current = jump_to_next_half_repeat_candidate(current)

    return total


# ============================================================================
# Part 2: Any Repeating Pattern (e.g., 11, 123123, 12341234)
# ============================================================================

def is_all_same_digit(num_str):
    """Check if all digits in the string are the same."""
    return len(set(num_str)) == 1


def is_three_char_repeating(num_str, length):
    """Check if string is made of repeating 3-character patterns."""
    if length % 3 != 0:
        return False
    parts = [num_str[i:i+3] for i in range(0, length, 3)]
    return len(set(parts)) == 1


def jump_from_small_number():
    """Handle numbers <= 10: jump directly to 11."""
    return "11"


def jump_from_odd_all_same_digit(current_str, length):
    """Handle odd-length numbers with all same digit (not 9).

    Example: 333 -> 3333 (add one more digit)
    """
    return str(int(current_str) + (10**length - 1) // 9)


def jump_from_two_digit(current_str):
    """Handle two-digit numbers (< 99).

    Examples:
    - 12 -> 22 (second digit >= first, increment first and repeat)
    - 21 -> 22 (second digit < first, just repeat first)
    """
    if current_str[1] >= current_str[0]:
        return str(int(current_str[0]) + 1) * 2
    else:
        return current_str[0] * 2


def jump_from_all_nines(length):
    """Handle numbers that are all 9s.

    Examples:
    - 99 -> 111 (even length: add one digit)
    - 999 -> 1010 (odd length: jump to next pattern)
    """
    if length % 2 == 0:
        return "1" * (length + 1)
    else:
        return str(10 ** (length // 2)) * 2


def jump_from_odd_length(current_str, length):
    """Handle odd-length numbers with various strategies.

    Tries in order:
    1. If divisible by 3: repeat first 3 chars
    2. If first digit repeatable: repeat first digit
    3. Otherwise: increment first digit and pad with zeros
    """
    # Try repeating first 3 chars if divisible by 3
    if length % 3 == 0 and length != 3 and not is_three_char_repeating(current_str, length):
        return current_str[:3] * (length // 3)

    # Check if we can repeat first digit
    first_digit = current_str[0]
    if int(first_digit) <= int(current_str[1]) and int(first_digit * length) <= int(current_str):
        if first_digit == '9':
            return str(10 ** (length // 2)) * 2
        else:
            return str(int(first_digit) + 1) + "0" * (length - 1)
    else:
        # Repeat first digit
        return first_digit * length


def find_next_even_pattern(current_str, length):
    """Find the next repeating pattern for even-length numbers.

    Generates all possible candidate patterns and returns the smallest one
    that's greater than the current number.
    """
    half = length // 2
    first_digit = current_str[0]

    candidates = []

    # Pattern 1: first digit repeated (e.g., 1234 -> 1111)
    candidates.append(int(first_digit * length))

    # Pattern 2: first digit repeated with one more digit (e.g., 1234 -> 11111)
    candidates.append(int(first_digit * (length + 1)))

    # Pattern 3: next digit with zeros (e.g., 1234 -> 20000)
    candidates.append(int(str(int(first_digit) + 1) + "0" * length))

    # Pattern 4: first two chars repeated (e.g., 1234 -> 1212)
    candidates.append(int(current_str[:2] * half))

    # Pattern 5: increment first two and repeat (e.g., 1234 -> 1313)
    candidates.append(int(str(int(current_str[:2]) + 1) * half))

    # Pattern 6: first half repeated (e.g., 1234 -> 1212)
    candidates.append(int(current_str[:half] * 2))

    # Pattern 7: increment first half and repeat (e.g., 1234 -> 1313)
    candidates.append(int(str(int(current_str[:half]) + 1) * 2))

    # Filter to only candidates greater than current
    valid = [c for c in candidates if c > int(current_str)]

    return str(min(valid))


def jump_to_next_repeating_candidate(current_str):
    """Find the next number that could be a repeating pattern.

    Uses various heuristics based on the number's properties to jump
    efficiently without checking every number.
    """
    length = len(current_str)
    current_int = int(current_str)

    # Small numbers
    if current_int <= 10:
        return jump_from_small_number()

    # Odd length with all same digit (not 9)
    if length % 2 == 1 and is_all_same_digit(current_str) and current_str[0] != '9':
        return jump_from_odd_all_same_digit(current_str, length)

    # Two-digit numbers
    if current_int < 99:
        return jump_from_two_digit(current_str)

    # All 9s
    if is_all_same_digit(current_str) and current_str[0] == '9':
        return jump_from_all_nines(length)

    # Odd length
    if length % 2 == 1:
        return jump_from_odd_length(current_str, length)

    # Even length
    return find_next_even_pattern(current_str, length)


def sum_repeating_patterns(ranges):
    """Find and sum all numbers in ranges that have any repeating pattern.

    Uses an optimization to jump between potential candidates instead of
    checking every number.
    """
    total = 0

    for start_str, end_str in ranges:
        end_int = int(end_str)
        current = start_str

        while int(current) <= end_int:
            if has_repeating_pattern(current):
                total += int(current)

            current = jump_to_next_repeating_candidate(current)

    return total


# ============================================================================
# Main
# ============================================================================

def main():
    # Parse inputs
    small_ranges = parse_input("small_input.txt")
    normal_ranges = parse_input("input.txt")

    print("=" * 60)
    print("Part 1: Half-Repeat Patterns (e.g., 1212, 333333)")
    print("=" * 60)

    start = time.time()
    small_result = sum_half_repeat_patterns(small_ranges)
    small_time = time.time() - start
    print(f"Small input:  {small_result:>12,} (expected: 1,227,775,554) [{small_time*1000:.2f}ms]")
    assert small_result == 1227775554, f"Expected 1227775554, got {small_result}"

    start = time.time()
    normal_result = sum_half_repeat_patterns(normal_ranges)
    normal_time = time.time() - start
    print(f"Normal input: {normal_result:>12,} (expected: 28,146,997,880) [{normal_time*1000:.2f}ms]")
    assert normal_result == 28146997880, f"Expected 28146997880, got {normal_result}"

    print("\n" + "=" * 60)
    print("Part 2: Any Repeating Pattern (e.g., 11, 123123, 12341234)")
    print("=" * 60)

    start = time.time()
    small_result = sum_repeating_patterns(small_ranges)
    small_time = time.time() - start
    print(f"Small input:  {small_result:>12,} (expected: 4,174,379,265) [{small_time*1000:.2f}ms]")
    assert small_result == 4174379265, f"Expected 4174379265, got {small_result}"

    start = time.time()
    normal_result = sum_repeating_patterns(normal_ranges)
    normal_time = time.time() - start
    print(f"Normal input: {normal_result:>12,} (expected: 40,028,128,307) [{normal_time*1000:.2f}ms]")
    assert normal_result == 40028128307, f"Expected 40028128307, got {normal_result}"

    print("\n" + "=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
