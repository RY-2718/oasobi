def main():
    n, k = map(int, input().split(" "))
    a = list(map(int, input().split(" ")))

    ans = 1 << 64

    for i in range(1 << n):
        total = 0
        colors = 0
        height = 0
        for j in range(n):
            if i >> j & 1:
                colors += 1
                if height >= a[j]:
                    total += height + 1 - a[j]
                    height += 1
            height = max(height, a[j])
        if colors >= k:
            ans = min(ans, total)

    print(ans)


if __name__ == "__main__":
    main()