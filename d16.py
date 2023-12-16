from aoc_lube import fetch, submit
from itertools import zip_longest

YEAR = 2023
DAY = 16

# In (x, y) movement format.
R = (1, 0)
D = (0, 1)
L = (-1, 0)
U = (0, -1)

MIRROR = {
    '/': {R: U, U: R, L: D, D: L},
    '\\': {R: D, D: R, L: U, U: L},
}

# Unfortunately, this function can't be cached as it can cause a RecursionError.
def simulate(x, y, direction):
    # Stores data as (abscissa (x), ordinate (y), direction).
    stack = [(x, y, direction)]
    seen = set()
    # Stores data as (abscissa, ordinate).
    energized = set()

    while stack:
        # x, y, (x movement (horizontal), y movement (vertical))
        x, y, (H, V) = stack.pop()

        while 0 <= x < ROW_LENGTH and 0 <= y < COL_LENGTH:
            _temp = (x, y, (H, V))
            if _temp in seen:
                break
            else:
                seen.add(_temp)

            energized.add((x, y))
            match data[y][x]:
                # Mirror case; (H, V) is the direction.
                case '/':
                    H, V = MIRROR['/'][(H, V)]
                case '\\':
                    H, V = MIRROR['\\'][(H, V)]
                # Splitter case.
                case '|':
                    if (H, V) in (R, L):
                        stack.append((x, y, U)) # Go through the upwards case later.
                        H, V = D # For now, go downwards.
                case '-':
                    if (H, V) in (D, U):
                        stack.append((x, y, L)) # Go through the leftwards case later.
                        H, V = R # For now, go rightwards.
            # Move.
            x += H
            y += V
    # Return the number of energized tiles.
    return len(energized)

def part_1():
    return simulate(0, 0, R)

def part_2():
    max_val = 0
    for direction in (U, D, L, R):
        if direction in (U, D):
            X_range = range(ROW_LENGTH)
            Y_range = () # Fill values later.
        else:
            X_range = () # Fill values later.
            Y_range = range(COL_LENGTH)

        if direction in (D, R):
            default = 0 # Both X and Y ranges can have 0.
        elif direction == U:
            default = COL_LENGTH - 1 # Y range only.
        else: # direction == L
            default = ROW_LENGTH - 1 # X range only.

        for x, y in zip_longest(X_range, Y_range, fillvalue=default):
            res = simulate(x, y, direction)
            if res > max_val:
                max_val = res
    # Done. Return.
    return max_val

if __name__ == '__main__':
    from sys import argv
    _DEBUG = '-d' in argv or '--debug' in argv

    inp = fetch(YEAR, DAY)
    data = inp.splitlines()

    ROW_LENGTH = len(data[0])
    COL_LENGTH = len(data)

    if _DEBUG:
        print("Part 1:", part_1())
        print("Part 2:", part_2())
    else:
        submit(YEAR, DAY, 1, part_1)
        submit(YEAR, DAY, 2, part_2)
