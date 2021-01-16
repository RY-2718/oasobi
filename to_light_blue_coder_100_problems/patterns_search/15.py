import math

memo = {}


def enumerate_patterns(parts):
    if len(parts) == 1:
        return [parts]

    if str(parts) in memo:
        return memo[str(parts)]

    patterns = []
    for i in range(len(parts)):
        patterns += [
            [parts[i]] + x for x in enumerate_patterns(parts[:i] + parts[i + 1 :])
        ]

    memo[str(parts)] = patterns
    return patterns


def main():
    n = int(input())
    points = []
    for i in range(n):
        points.append(list(map(int, input().split(" "))))

    patterns = enumerate_patterns(list(range(n)))

    sum = 0
    for pattern in patterns:
        _sum = 0
        for i in range(n - 1):
            start = points[pattern[i]]
            end = points[pattern[i + 1]]
            dist = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            _sum += dist
        sum += _sum
    print(sum / len(patterns))


if __name__ == "__main__":
    main()