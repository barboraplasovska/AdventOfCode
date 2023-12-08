import re

def readFile(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    return lines

hist_1 = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
hist_2 = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
hist_len = len(hist_1)

def histogram(a, hist_a, hist):
    for i in range(len(a)):
        if a[i] in hist:
            hist_a[hist.index(a[i])][1] += 1
    return hist_a

def strongerLetter(a, b, hist):
    index_a = hist.index(a)
    index_b = hist.index(b)
    if index_a < index_b:
        return True
    else:
        return False
    
def identifyHand(hist_a):
    
    ## 5 cards
    if any(hist_a[i][1] == 5 for i in range(hist_len)):
        return 0
    
    ## 4 cards
    if any(hist_a[i][1] == 4 for i in range(hist_len)):
        return 1
        
    ## Full house
    if any(hist_a[i][1] == 3 for i in range(hist_len)) and any(hist_a[i][1] == 2 for i in range(hist_len)):
        return 2
        
    ## 3 cards
    if any(hist_a[i][1] == 3 for i in range(hist_len)):
        return 3
        
    ## 2 pairs
    if sum(hist_a[i][1] == 2 for i in range(hist_len)) == 2:
        return 4
        
    ## 1 pair
    if sum(hist_a[i][1] == 2 for i in range(hist_len)) == 1:
        return 5
        
    ## High card
    return 6

def getHistogram(a, hist):
    a = a.split(" ")[0]
    hist_a = [[x, 0] for x in hist]
    return histogram(a, hist_a, hist)

def makeJokerUseful(a, hist_a, hist):
    hand = identifyHand(hist_a)
    nb_joker = hist_a[-1][1]

    if nb_joker == 0 or hand == 0:
        return hand

    best_hand = hand
    for i in range(hist_len):
        new_word = a.replace('J', hist_a[i][0])
        new_hist = getHistogram(new_word, hist)
        new_hand = identifyHand(new_hist)
        if new_hand < best_hand:
            best_hand = new_hand
    
    return best_hand

def compare(a, b, hist, part):
    hist_a = getHistogram(a, hist)
    hist_b = getHistogram(b, hist)

    hand_a = 6
    hand_b = 6

    if part == 1:
        hand_a = identifyHand(hist_a)
        hand_b = identifyHand(hist_b)
    else:
        hand_a = makeJokerUseful (a, hist_a, hist)
        hand_b = makeJokerUseful(b, hist_b, hist)

    if hand_a < hand_b:
        return True
    elif hand_a > hand_b:
        return False

    i = 0
    while a[i] == b[i]:
        i += 1
    return strongerLetter(a[i], b[i], hist)

def merge(left, right, hist, part):
    if len(left) == 0:
        return right
    
    if len(right) == 0:
        return left

    result = []
    index_left = index_right = 0

    while len(result) < len(left) + len(right):
        if compare(left[index_left],right[index_right], hist, part):
            result.append(left[index_left])
            index_left += 1
        else:
            result.append(right[index_right])
            index_right += 1

        if index_right == len(right):
            result += left[index_left:]
            break

        if index_left == len(left):
            result += right[index_right:]
            break

    return result

def merge_sort(array, hist, part = 1):
    if len(array) < 2:
        return array

    midpoint = len(array) // 2

    return merge(
        left=merge_sort(array[:midpoint], hist, part),
        right=merge_sort(array[midpoint:], hist, part),
        hist=hist,
        part=part)

def part1(lines):
    hist = hist_1
    lines = merge_sort(lines, hist)
    len_lines = len(lines)
    res = 0
    for i in range(len(lines)):
        bid = lines[i].split(" ")[1]
        res += int(bid) * len_lines
        len_lines -= 1

    return res

def part2(lines):
    hist = hist_2
    lines = merge_sort(lines, hist, 2)
    len_lines = len(lines)
    res = 0
    for i in range(len(lines)):
        bid = lines[i].split(" ")[1]
        res += int(bid) * len_lines
        len_lines -= 1

    return res


def main():
    lines = readFile("input.txt")
    #print("part 1: " + str(part1(lines)))
    print("part 2: " + str(part2(lines)))
main()