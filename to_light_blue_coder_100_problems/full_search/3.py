s = input()
length = 0

for i in range(0, len(s)):
    breaked = False
    for j in range(i, len(s)):
        if not (s[j] in ["A", "C", "G", "T"]):
            length = max(length, j - i)
            breaked = True
            break
    if not breaked:
        length = max(length, len(s) - i)

print(length)