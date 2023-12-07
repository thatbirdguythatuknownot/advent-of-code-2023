from aoc_lube import fetch, submit

YEAR = 2023
DAY = 7

CARDS = "J23456789TJQKA"
J_VALUE = CARDS.find('J')
BASE = len(CARDS)
HIGH_DIGIT = BASE ** 5

def keyval(hand, is_part_2=True):
    key_val = 0
    power = 4

    for card in hand:
        if is_part_2:
            value = CARDS.find(card)
        else:
            value = CARDS.rfind(card)

        key_val += value * BASE**power
        power -= 1

    return key_val

def get_sort_key(is_part_2):
    def sort_key(element):
        hand, _ = element
        hand_set = set(hand)

        if is_part_2:
            hand_set -= {'J'}
            subtract_val = hand.count('J')
        else:
            subtract_val = 0

        hand_key_val = keyval(hand, is_part_2=is_part_2)
        match len(hand_set):
            case 1 | 0:
                return hand_key_val + 6*HIGH_DIGIT # 5-of-a-kind

            case 2:
                counts = map(hand.count, hand_set)
                if 4 - subtract_val in counts:
                    return hand_key_val + 5*HIGH_DIGIT # 4-of-a-kind
                return hand_key_val + 4*HIGH_DIGIT # full house

            case 3:
                counts = map(hand.count, hand_set)
                if 3 - subtract_val in counts:
                    return hand_key_val + 3*HIGH_DIGIT # 3-of-a-kind
                return hand_key_val + 2*HIGH_DIGIT # 2-pair

            case 4:
                return hand_key_val + HIGH_DIGIT # 1-pair

            case _:
                return hand_key_val # high card

    return sort_key

def get_solve_func(part):
    is_part_2 = part == 2
    def solver():
        key = get_sort_key(is_part_2=is_part_2)
        sorted_data = sorted(data, key=key)
        return sum(rank * bid
                   for rank, (_, bid) in enumerate(sorted_data, start=1))
    return solver

if __name__ == '__main__':
    inp = fetch(YEAR, DAY)
    data = [(hand, int(bid))
            for line in inp.splitlines()
            for hand, bid in [line.split()]]
    submit(YEAR, DAY, 1, get_solve_func(part=1))
    submit(YEAR, DAY, 2, get_solve_func(part=2))
