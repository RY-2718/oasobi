n = int(input())
s = input()

answers = set()

searched_first = set()
for i in range(0, n):
    if s[i] in searched_first:
        continue
    searched_first.add(s[i])

    searched_second = set()
    for j in range(i + 1, n):
        if s[j] in searched_second:
            continue
        searched_second.add(s[j])

        for k in range(j + 1, n):
            answers.add("{0}{1}{2}".format(s[i], s[j], s[k]))

print(len(answers))
