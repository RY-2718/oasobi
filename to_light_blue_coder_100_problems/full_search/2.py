import math

n = int(input())
count = 0

for i in range(1, n + 1, 2):
    divisors = 0
    for j in range(1, int(math.sqrt(i)) + 1):
        if i % j == 0:
            if j * j == i:
                divisors += 1
            else:
                divisors += 2
    if divisors == 8:
        count += 1

print(count)