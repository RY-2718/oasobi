from bisect import bisect_left


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

    def powered_length(self):
        return self.x ** 2 + self.y ** 2


def main():
    n = int(input())

    p = []

    for i in range(n):
        x, y = map(int, input().split(" "))
        p.append(Vector2D(x, y))

    POINT_MAX = 65535
    p.append(Vector2D(POINT_MAX, POINT_MAX))
    p = sorted(p)

    ans = 0

    for i in range(n):
        for j in range(i + 1, n):
            a = p[i]
            b = p[j]

            l = (b - a).powered_length()
            if l <= ans:
                continue

            c1 = Vector2D(b.x - (b.y - a.y), b.y + (b.x - a.x))
            d1 = Vector2D(a.x - (b.y - a.y), a.y + (b.x - a.x))
            c2 = Vector2D(b.x + (b.y - a.y), b.y + (a.x - b.x))
            d2 = Vector2D(a.x + (b.y - a.y), a.y + (a.x - b.x))

            if (c1 == p[bisect_left(p, c1)] and d1 == p[bisect_left(p, d1)]) or (
                c2 == p[bisect_left(p, c2)] and d1 == p[bisect_left(p, d2)]
            ):
                ans = max(ans, l)

    print(ans)


if __name__ == "__main__":
    main()