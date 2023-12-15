from aoc_lube import fetch, submit
import re

YEAR = 2023
DAY = 15

def hash_(string):
    hash_num = 0
    for char in string:
        hash_num += ord(char)
        hash_num *= 17
        hash_num %= 256
    return hash_num

def part_1():
    return sum(map(hash_, data))

def part_2():
    boxes = [{} for _ in range(256)]

    for step in data:
        match re.split(r"=|-", step):
            case label, "":
                # `<label>-` case
                # If the key doesn't exist, using `dict.pop()` with the
                # optional second argument won't error.
                boxes[hash_(label)].pop(label, None)
            case label, focal_len_str:
                # `<label>=<focal length>` case
                boxes[hash_(label)][label] = int(focal_len_str)

    focus_power = 0
    for box_idx, box in enumerate(boxes):
        for lens_idx, focal_len in enumerate(box.values()):
            focus_power += (box_idx + 1) * (lens_idx + 1) * focal_len

    return focus_power

if __name__ == '__main__':
    from sys import argv
    _DEBUG = '-d' in argv or '--debug' in argv

    inp = fetch(YEAR, DAY)
    data = inp.split(',')

    if _DEBUG:
        print("Part 1:", part_1())
        print("Part 2:", part_2())
    else:
        submit(YEAR, DAY, 1, part_1)
        submit(YEAR, DAY, 2, part_2)
