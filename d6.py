from aoc_lube import fetch, submit
from math import prod

YEAR = 2023
DAY = 6

def get_solve_func(part):
    is_part_2 = part == 2
    def solver():
        if is_part_2:
            times = [int("".join(data_time))]
            dists = [int("".join(data_dist))]
        else:
            times = list(map(int, data_time))
            dists = list(map(int, data_dist))

        results = []
        for time, dist in zip(times, dists):
            exceeding = 0

            for i in range(time + 1):
                if i*(time - i) > dist:
                    exceeding += 1

            results.append(exceeding)
        return prod(results)
    return solver

if __name__ == '__main__':
    inp = fetch(YEAR, DAY)

    line_time, line_dist = inp.splitlines()
    data_time = line_time.split()[1:]
    data_dist = line_dist.split()[1:]

    submit(YEAR, DAY, 1, get_solve_func(part=1))
    submit(YEAR, DAY, 2, get_solve_func(part=2))
