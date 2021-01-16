def is_bulb_lightning(bulb, switch, power):
    switch_count = 0
    for i in bulb:
        switch_count += switch[i - 1]
    return switch_count % 2 == power


def main():
    n, m = map(int, input().split(" "))
    bulbs = []
    for i in range(m):
        bulb = list(map(int, input().split(" ")))[1:]
        bulbs.append(bulb)
    powers = list(map(int, input().split(" ")))

    switchs = []
    for pattern in range(2 ** n):
        switch = []
        for i in range(n):
            switch.append((pattern >> i) % 2)
        switchs.append(switch)

    ans = 0

    for switch in switchs:
        ok = True
        for i in range(m):
            if not is_bulb_lightning(bulbs[i], switch, powers[i]):
                ok = False
                break
        if ok:
            ans += 1

    print(ans)


if __name__ == "__main__":
    main()