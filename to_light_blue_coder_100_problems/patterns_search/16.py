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


def binary_search(l, v, isOK):
    ng = -1
    ok = len(l)

    while abs(ng - ok) > 1:
        mid = (ng + ok) // 2
        if isOK(l, mid, v):
            ok = mid
        else:
            ng = mid

    return ok


def main():
    n = int(input())
    p = list(map(int, input().split(" ")))
    q = list(map(int, input().split(" ")))

    patterns = enumerate_patterns(list(range(1, n + 1)))

    def _isOK(l, mid, v):
        m = l[mid]
        for i in range(len(m)):
            if v[i] > m[i]:
                return False
            elif v[i] < m[i]:
                return True
        return True

    i_p = binary_search(patterns, p, _isOK)
    i_q = binary_search(patterns, q, _isOK)
    print(abs(i_p - i_q))


if __name__ == "__main__":
    main()