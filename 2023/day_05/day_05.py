import numpy as np

def readFile(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    return lines

def part1(lines):
    seeds = lines[0].split(" ")
    seeds.pop(0)
    seeds = [int(x) for x in seeds]
    res = seeds
    M = [False] * len(seeds)

    first = True
   
    i = 2
    while i < len(lines):
        if lines[i] == "" or lines[i][0].isalpha():
            i += 1
            first = False
            M = [False] * len(seeds)
            if lines[i][0].isalpha():
                print(lines[i])
            continue

        nbs = lines[i].split(" ")
        dest_start = int(nbs[0])
        source_start = int(nbs[1])
        range = int(nbs[2])

        dest = np.arange(dest_start, dest_start + range)
        source = np.arange(source_start, source_start + range)

        j = 0
        while j < len(seeds):
            if first:
                if seeds[j] in source and not M[j]:
                    res[j] = dest[np.where(source == seeds[j])][0]
                    M[j] = True
            else:
                if res[j] in source and not M[j]:
                    res[j] = dest[np.where(source == res[j])][0]
                    M[j] = True
            j += 1

        i += 1

    return np.min(res)
        
def parse_input(lines):
    seeds = list(int(s) for s in lines.pop(0).split(': ')[1].split())
    lines.pop(0)
    maps = []
    while lines:
        line = lines.pop(0)
        if line.endswith('map:'):
            current = []
            continue
        if line == '':
            maps.append(current)
            continue
        current.append(tuple(int(n) for n in line.split()))
    maps.append(current)
    return seeds, maps

def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)

def map_range(seed_range, maps):
        res = []
        seed_start, seed_len = seed_range
        for dest, source, range_len in sorted(maps, key=lambda x:x[1]):
            if seed_start >= source and seed_start < source + range_len:
                res_start = seed_start + dest - source
                
                if source + range_len < seed_start + seed_len:
                    new_seed_len = seed_start + seed_len - source - range_len
                    res.append((res_start, seed_len - new_seed_len))
                    seed_len = new_seed_len
                    seed_start = source + range_len
                else:
                    res.append((res_start, seed_len))
                    
        if not res:
            res.append(seed_range)
        return res

def part2(lines):
    seeds, maps = parse_input(lines)
    res = []
    for seed_pair in pairwise(seeds):
        seed_ranges = [seed_pair]
        for map in maps:
            new_s = []
            for s in seed_ranges:
                new_s.extend(map_range(s, map))
            seed_ranges = new_s[:]
        res.append(min(x for x, _ in seed_ranges))
    return min(res)

def main():
    lines = readFile("input.txt")
    print("part 1: " + str(part1(lines)))
    print("part 2: " + str(part2(lines)))
main()



