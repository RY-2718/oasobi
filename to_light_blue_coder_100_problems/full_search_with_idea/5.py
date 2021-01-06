a, b, c, x, y = map(int, input().split(" "))

sum = 0

sum += min(x, y) * min(a + b, c * 2)

if x >= y:
    sum += (x - y) * min(a, c * 2)
else:
    sum += (y - x) * min(b, c * 2)

print(sum)
