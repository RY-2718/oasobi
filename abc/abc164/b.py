a, b, c, d = map(int, input().split(" "))

turn = 0

while a > 0 and c > 0:
    if turn % 2 == 0:
        c -= b
    else:
        a -= d
    turn += 1

if turn % 2 == 0:
    print("No")
else:
    print("Yes")
