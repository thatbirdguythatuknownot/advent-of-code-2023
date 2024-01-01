from aoc_lube import fetch, submit
import itertools
import re
import math
from collections import defaultdict

YEAR = 2023
DAY = 24

def part_1(LEAST=200000000000000, MOST=400000000000000):
    count = 0
    visited = set()
    for i, (x1, y1, _, vx1, vy1, _) in enumerate(data):
        m1 = vy1 / vx1
        for j, (x2, y2, _, vx2, vy2, _) in enumerate(data):
            if i == j:
                continue
            if (i, j) in visited:
                continue
            # Add both since, for example, it might traverse (1, 3)
            # and then also traverse (3, 1) after... they're the same thing
            visited.add((i, j))
            visited.add((j, i))
            m2 = vy2 / vx2
            if m1 == m2:
                continue
            # https://math.stackexchange.com/questions/1990698
            h = (m1*x1 - m2*x2 - y1 + y2) / (m1 - m2)
            k = m1*(h - x1) + y1
            if LEAST <= h <= MOST and LEAST <= k <= MOST:
                if (h - x1)/vx1 >= 0 and (h - x2)/vx2 >= 0:
                    count += 1
    return count

def factors(n, choice_set=None):
    if choice_set is None:
        choice_set = set()
        for i in range(1, int(math.sqrt(abs(n))) + 1):
            if not n % i:
                choice_set.add(i)
                choice_set.add(-i)
                choice_set.add(i := n // i)
                choice_set.add(-i)
        return choice_set
    not_factors = set()
    for factor in choice_set:
        if n % factor:
            not_factors.add(factor)
    return choice_set - not_factors

def part_2():
    velocity = [0, 0, 0]
    for axis in 0, 1, 2:
        same_velos = defaultdict(list)
        for hail in data:
            same_velos[hail[3 + axis]].append(hail)
        possibles = None
        for world_velo, hails in same_velos.items():
            relative_rock_velos = None
            min_bound = math.inf
            if len(hails) == 1:
                continue
            for hail_0, hail_1 in itertools.pairwise(hails):
                relative_rock_velos = factors(
                    dist := abs(hail_0[axis] - hail_1[axis]),
                    relative_rock_velos
                )
                if dist < min_bound:
                    min_bound = dist
            world_rock_velos = {
                relative_velo + world_velo
                for relative_velo in relative_rock_velos
                if -min_bound <= relative_velo <= min_bound
            }
            if possibles is None:
                possibles = world_rock_velos
            else:
                possibles &= world_rock_velos
        assert len(possibles) == 1
        velocity[axis] = possibles.pop()
    valid_axis = -1
    valid_point = None
    for hail in data:
        for axis in 0, 1, 2:
            if hail[3 + axis] == velocity[axis]:
                valid_point = hail[axis]
                valid_axis = axis
                break
    assert valid_axis == -1
    valid_points = [0, 0, 0]
    hail0 = data[0]
    time = (valid_point - hail0[valid_axis]) // (hail0[3 + valid_axis] - velocity[valid_axis])
    for axis in 0, 1, 2:
        valid_points[axis] = hail0[axis] + time*(hail0[3 + axis] - velocity[axis])
    return sum(valid_points)

if __name__ == '__main__':
    from sys import argv
    _DEBUG = '-d' in argv or '--debug' in argv

    inp = fetch(YEAR, DAY)
    data = [re.findall(r"-?\d+", x) for x in inp.splitlines()]

    if _DEBUG:
        print("Part 1:", part_1(LEAST=7, MOST=27))
        print("Part 2:", part_2())
    else:
        submit(YEAR, DAY, 1, part_1)
        submit(YEAR, DAY, 2, part_2)
