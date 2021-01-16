from bisect import bisect_left


def main():
    n = int(input())
    a = list(map(int, input().split(" ")))
    q = int(input())
    m = list(map(int, input().split(" ")))

    bits = []
    for i in range(2 ** n):
        bit = []
        for digit in range(n):
            bit.append((i // (2 ** digit)) % 2)
        bits.append(bit)

    sums = []
    for bit in bits:
        sum = 0
        for i in range(n):
            sum += a[i] * bit[i]
        sums.append(sum)

    sums.sort()

    for mi in m:
        i = bisect_left(sums, mi)
        if i >= 0 and i < len(sums) and mi == sums[i]:
            print("yes")
        else:
            print("no")


if __name__ == "__main__":
    main()