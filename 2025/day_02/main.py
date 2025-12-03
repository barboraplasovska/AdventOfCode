import time


def read_file(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = f.read()

    ranges = data.strip().split(",")

    return ranges

def is_invalid_id1(id):
    l = len(id)
    if l % 2 != 0:
        return False

    return id[:l//2] == id[l//2:]

def part_one(ranges, debug):
    res = 0
    for range in ranges:
        range_split = range.split("-")
        first, last = range_split[0], range_split[1]
        
        curr = first

        while int(curr) <= int(last):
            l = len(curr)
            if is_invalid_id1(curr):
                if debug:
                    print("invalid number:", curr)
                res += int(curr)

                # go to next number
                if curr.count("9") == l:
                    curr = str(10 ** (l // 2)) * 2
                else:
                    step = 10 ** (l // 2) + 1
                    curr = str(int(curr) + step)
            else:
                if l % 2 == 0:
                    if int(curr[:l//2]) < int(curr[l//2:]):
                        first_half = int(curr[:l//2]) + 1
                        curr = f"{first_half}{first_half}"
                    else: 
                        curr = f"{curr[:l//2]}{curr[:l//2]}"
                else:
                    first_digit = int(curr[0])
                    if first_digit == 9:
                        curr = str((10 ** (l // 2 ))) * 2
                    elif l == 1:
                        curr = "11"
                    elif curr[0] == '1':
                        curr = curr[:(l + 1)//2] * 2
                    else:
                        curr = str((10 ** (l // 2 ))) * 2
    
    return res

def is_invalid_id2(id):
    l = len(id)

    if l == 1:
        return False

    if id.count(id[0]) == l:
        return True # All are the same
    
    curr = l // 2
    while curr > 0:
        if l % curr == 0: # if i can divide the string into chunks of curr
            parts = [id[i:i+curr] for i in range(0, l, curr)]
            if len(set(parts)) == 1:
                return True
        curr -= 1
    return False

def find_possible_even_nb(nb, l):
    # aaaa
    case1 = nb[0] * l

    # aaaaa
    case2 = nb[0] * (l + 1)

    # [a+1] 000
    case3 = str( int(nb[0]) + 1 ) + l * "0"

    # abab
    case4 = nb[:2] * (l // 2)

    # a[b+1] a[b+1]
    case5 = str(int(nb[:2]) + 1 ) * (l // 2)

    # abc abc / abcd abcd ....
    unit = l // 2
    case6 = nb[:unit] * 2

    # ab[c+1] ab[c+1]
    case7 = str(int(nb[:unit]) + 1 ) * 2

    cases = [case1, case2, case3, case4, case5, case6, case7]
    cases_int = [int(x) for x in cases]
    cases_int = [x for x in cases_int if x > int(nb)]

    return str(min(cases_int))

def is_abc_repeating(nb, l):
    parts = [nb[i:i+3] for i in range(0, l, 3)]

    return len(set(parts)) == 1

def part_two(ranges, debug):
    res = 0
    for range in ranges:
        range_split = range.split("-")
        first, last = range_split[0], range_split[1]
        
        curr = first

        while int(curr) <= int(last):
            if debug:
                print("\n\n first", first, "curr", curr, "last", last)

            l = len(curr)

            if is_invalid_id2(curr):
                if debug:
                    print("invalid number:", curr, "for range:", range)
                res += int(curr)
            
            # go to next number
            if int(curr) <= 10:
                if debug:
                    print("a")
                curr = "11"
            elif l % 2 == 1 and len(set(curr)) == 1 and curr[0] != '9': # if all digits are the same and not 9
                if debug:
                    print("b")
                curr = str(int(curr) + (10**l - 1) // 9)
            elif int(curr) < 99:
                if curr[1] >= curr[0]:
                    curr = str(int(curr[0]) + 1) * 2
                else:
                    curr = curr[0] * 2
                if debug:
                    print("bb")
            elif curr.count("9") == l: # only 9
                if l % 2 == 0: # if the digit count is even
                    if debug:
                        print("c")
                    curr = (l + 1) * "1" # 99 -> 111
                else:
                    if debug:
                        print("d")
                    curr = str((10 ** (l // 2 ))) * 2 # 999 -> 1010
            elif l % 2 == 1: # if the digit count is odd
                if l % 3 == 0 and l != 3 and not is_abc_repeating(curr, l): # if divisible by 3
                    if debug:
                        print("e")
                    curr = curr[:3] * (l // 3)
                elif int(curr[0]) <= int(curr[1]) and int(curr[0] * l) <= int(curr):
                    if debug:
                        print("ee")
                    if curr[0] == "9":
                        curr = str(10 ** (l//2)) * 2
                    else:
                        curr = str(int(curr[0]) + 1) + (l-1) * "0"
                else:
                    if debug:
                        print("f")
                    curr = curr[0] * l # 70111 -> 77777
            else: # if the digit count is even
                if debug:
                    print("g")
                curr = find_possible_even_nb(curr, l)

            if debug:
                print("next curr", curr)
    
    return res


def test_invalid_id():
    print(is_invalid_id2("a"))
    print(is_invalid_id2("aaa"))
    print(is_invalid_id2("aaaa"))
    print(is_invalid_id2("abab"))
    print(is_invalid_id2("ababab"))
    print(is_invalid_id2("abcabc"))
    print(is_invalid_id2("abcdabcd"))
    print(is_invalid_id2("abcdabcdabcd"))
    print(is_invalid_id2("ababababab"))
    print(is_invalid_id2("11"))
    print(is_invalid_id2("22"))
    print(is_invalid_id2("99"))
    print(is_invalid_id2("999"))
    print(is_invalid_id2("1010"))
    print(is_invalid_id2("1188511885"))
    print(is_invalid_id2("222222"))
    print(is_invalid_id2("446446"))
    print(is_invalid_id2("38593859"))
    print(is_invalid_id2("565656"))
    print(is_invalid_id2("824824824"))
    print(is_invalid_id2("2121212121"))


def main():
    ranges_small = read_file("small_input.txt")
    ranges_normal = read_file("input.txt")

    print("=" * 60)
    print("PART 1: Half-Repeat Patterns")
    print("=" * 60)

    start = time.time()
    small_result = part_one(ranges_small, False)
    small_time = time.time() - start
    print(f"Small input:  {small_result:>12,} (expected: 1,227,775,554) [{small_time*1000:.2f}ms]")
    assert small_result == 1227775554, f"Expected 1227775554, got {small_result}"

    start = time.time()
    normal_result = part_one(ranges_normal, False)
    normal_time = time.time() - start
    print(f"Normal input: {normal_result:>12,} (expected: 28,146,997,880) [{normal_time*1000:.2f}ms]")
    assert normal_result == 28146997880, f"Expected 28146997880, got {normal_result}"

    print("\n" + "=" * 60)
    print("PART 2: Any Repeating Pattern")
    print("=" * 60)

    start = time.time()
    small_result = part_two(ranges_small, False)
    small_time = time.time() - start
    print(f"Small input:  {small_result:>12,} (expected: 4,174,379,265) [{small_time*1000:.2f}ms]")
    assert small_result == 4174379265, f"Expected 4174379265, got {small_result}"

    start = time.time()
    normal_result = part_two(ranges_normal, False)
    normal_time = time.time() - start
    print(f"Normal input: {normal_result:>12,} (expected: 40,028,128,307) [{normal_time*1000:.2f}ms]")
    assert normal_result == 40028128307, f"Expected 40028128307, got {normal_result}"

    print("\n" + "=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)

main()