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


def print_queens(pattern):
    for p in pattern:
        print("." * (p) + "Q" + "." * (8 - p - 1))


def main():
    k = int(input())
    deployed = []
    for i in range(k):
        deployed.append(list(map(int, input().split(" "))))

    patterns = enumerate_patterns(list(range(8)))

    for pattern in patterns:
        ok = True
        for d in deployed:
            if pattern[d[0]] != d[1]:
                ok = False
                break
        if not ok:
            continue

        for r, c in enumerate(pattern):
            _r = r + 1
            _c = c + 1
            while _r < 8 and _c < 8:
                if pattern[_r] == _c:
                    ok = False
                    break
                _r += 1
                _c += 1
            if not ok:
                break
        if not ok:
            continue

        for r, c in enumerate(pattern):
            _r = r + 1
            _c = c + 1
            while _r < 8 and _c < 8:
                if pattern[_r] == _c:
                    ok = False
                    break
                _r += 1
                _c += 1
            if not ok:
                break

            _r = r + 1
            _c = c - 1
            while _r < 8 and _c >= 0:
                if pattern[_r] == _c:
                    ok = False
                    break
                _r += 1
                _c -= 1
            if not ok:
                break

            _r = r - 1
            _c = c + 1
            while _r >= 0 and _c < 8:
                if pattern[_r] == _c:
                    ok = False
                    break
                _r -= 1
                _c += 1
            if not ok:
                break

            _r = r - 1
            _c = c - 1
            while _r >= 0 and _c >= 0:
                if pattern[_r] == _c:
                    ok = False
                    break
                _r -= 1
                _c -= 1
            if not ok:
                break
        if not ok:
            continue

        if ok:
            print_queens(pattern)
            return


if __name__ == "__main__":
    main()