n, m = map(int, input().split(" "))
a = []
score = 0

for i in range(n):
    a.append([int(x) for x in input().split(" ")])

for i in range(m):
    for j in range(i + 1, m):
        local_score = 0
        for k in range(n):
            local_score += max(a[k][i], a[k][j])
        score = max(score, local_score)

print(score)