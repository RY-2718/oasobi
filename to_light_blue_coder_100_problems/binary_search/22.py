import math


def main():
    p = float(input())

    a = 2 / 3 * math.log(2)

    def dtdx(x):
        return 1 - a * p * (2 ** (-2 * x / 3))

    def isOK(x):
        return dtdx(x) > 0.0

    x = binary_search(isOK)

    if x < 0:
        ans = p
    else:
        ans = x + p / 2 ** (x / 1.5)

    print(ans)


def binary_search(isOK):
    ng = -1
    ok = int(1e9)

    for i in range(10000):
        mid = ng + (ok - ng) / 2

        if isOK(mid):
            ok = mid
        else:
            ng = mid

    return ok


if __name__ == "__main__":
    main()
