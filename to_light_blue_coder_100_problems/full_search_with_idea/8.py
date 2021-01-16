def main():
    n = int(input())
    a = []
    b = []
    ab = []

    for i in range(n):
        _a, _b = map(int, input().split(" "))
        a.append(_a)
        b.append(_b)
        ab.append(_a)
        ab.append(_b)

    ab.sort()

    # 愚直解（部分点をもらえる仕様）
    ans = 2 * n * 10 ** 9
    for i in range(0, len(ab)):
        start = ab[i]
        for j in range(i+1, len(ab)):
            end = ab[j]
            sum = 0
            for k in range(n):
                tmp = abs(a[k] - start) + abs(b[k] - a[k]) + abs(b[k] - end)
                sum += tmp
            ans = min(ans, sum)

    print(ans)


if __name__ == "__main__":
    main()