n, m = map(int, input().split(" "))

relations = []
for i in range(m):
    relations.append(list(map(int, input().split(" "))))

parties = []
for i in range(2 ** n):
    party = []
    for j in range(n):
        digit = (i >> j) % 2
        if digit == 1:
            party.append(j + 1)
    if len(party) > 1:
        parties.append(party)

ans = 1

for party in parties:
    valid = True
    for i in range(len(party)):
        for j in range(i + 1, len(party)):
            if not [party[i], party[j]] in relations:
                valid = False
                break
        if not valid:
            break
    if valid:
        ans = max(ans, len(party))

print(ans)
