def main():
    n = int(input())
    a = list(map(int, input().split(" ")))
    b = list(map(int, input().split(" ")))
    c = list(map(int, input().split(" ")))

    a.sort()
    b.sort()
    c.sort()

    def lt(arr, value, mid):
        return arr[mid] > value

    def le(arr, value, mid):
        return arr[mid] >= value

    ans = 0
    for bb in b:
        a_i = binary_search(a, bb, le)
        c_i = binary_search(c, bb, lt)
        ans += a_i * (n - c_i)

    print(ans)


def binary_search(arr, value, isOK):
    ng = -1
    ok = len(arr)

    while abs(ok - ng) > 1:
        mid = ng + (ok - ng) // 2

        if isOK(arr, value, mid):
            ok = mid
        else:
            ng = mid

    return ok


if __name__ == "__main__":
    main()