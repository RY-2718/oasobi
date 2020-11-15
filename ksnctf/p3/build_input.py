def build():
    p = [
        70,
        152,
        195,
        284,
        475,
        612,
        791,
        896,
        810,
        850,
        737,
        1332,
        1469,
        1120,
        1470,
        832,
        1785,
        2196,
        1520,
        1480,
        1449,
    ]
    s = ""
    for i in range(len(p)):
        s += chr(p[i] // (i + 1))

    # FLAG_fqpZUCoqPb4izPJE
    return s


def main():
    print(build())


if __name__ == "__main__":
    main()