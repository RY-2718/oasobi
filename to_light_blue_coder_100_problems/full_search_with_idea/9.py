class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.x < other.x if self.x != other.x else self.y < other.y

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)


def binary_search(arr, v, isOK):
    ng = -1
    ok = len(arr)

    while abs(ok - ng) > 1:
        mid = (ok + ng) // 2

        if isOK(arr, mid, v):
            ok = mid
        else:
            ng = mid

    return ok


def isOK(arr, mid, v):
    return arr[mid] >= v


def main():
    m = int(input())
    sign = []
    for i in range(m):
        x, y = map(int, input().split(" "))
        sign.append(Vector2D(x, y))
    sign.sort()

    n = int(input())
    stars = []
    for i in range(n):
        x, y = map(int, input().split(" "))
        stars.append(Vector2D(x, y))
    stars.sort()

    for i in range(n - m + 1):
        d = stars[i] - sign[0]
        found = True
        for j in range(1, m):
            translated = sign[j] + d
            key = binary_search(stars, translated, isOK)
            if key < 0 or key >= n or stars[key] != translated:
                found = False
                break

        if found:
            print("{} {}".format(d.x, d.y))
            return


if __name__ == "__main__":
    main()