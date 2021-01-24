def binary_search(ls, key, isOK):
    ng = -1
    ok = len(ls)

    while abs(ng - ok) > 1:
        mid = (ok + ng) // 2

        if isOK(ls, key, mid):
            ok = mid
        else:
            ng = mid

    return ok


def main():
    n = int(input())
    s = list(map(int, input().split(" ")))
    q = int(input())
    t = list(map(int, input().split(" ")))

    def isOK(ls, key, mid):
        return ls[mid] >= key

    c = 0
    for tt in t:
        i = binary_search(s, tt, isOK)
        if i >= 0 and i < len(s) and s[i] == tt:
            c += 1

    print(c)


if __name__ == "__main__":
    main()