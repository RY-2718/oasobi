from functools import reduce

n, m = map(int, input().split(" "))
a = list(map(int, input().split(" ")))
sum = reduce(lambda x, y: x + y, a)

print(max(n - sum, -1))
