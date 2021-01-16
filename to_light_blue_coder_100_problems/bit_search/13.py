from functools import reduce
import copy


def turn_columns(crackers):
    r = len(crackers)
    counts = reduce(lambda a, b: [x + y for (x, y) in zip(a, b)], crackers)
    return reduce(lambda a, b: a + max(b, r - b), counts)


def main():
    r, c = map(int, input().split(" "))

    crackers = []
    for i in range(r):
        crackers.append(list(map(int, input().split(" "))))

    # ここで「裏返したせんべい」をメモしないと TLE
    turned_crackers = []
    for i in range(r):
        turned_crackers.append([x ^ 1 for x in crackers[i]])

    raw_patterns = []
    for i in range(2 ** r):
        raw_pattern = []
        for j in range(r):
            raw_pattern.append((i >> j) % 2)
        raw_patterns.append(raw_pattern)

    max_crackers = 0
    for raw_pattern in raw_patterns:
        _crackers = []

        for i in range(r):
            if raw_pattern[i] == 0:
                _crackers.append(crackers[i])
            else:
                _crackers.append(turned_crackers[i])

        max_crackers = max(max_crackers, turn_columns(_crackers))

    print(max_crackers)


if __name__ == "__main__":
    # crackers = [[0, 1, 0, 1, 0], [1, 0, 0, 0, 1]]
    # print(turn_columns(crackers))

    main()
