def ccyper(str: str, offset: int) -> str:
    res = ""
    for s in str:
        if "A" <= s and s <= "Z":
            o = ord(s) + offset
            if o > ord("Z"):
                o -= ord("Z") - ord("A") + 1
            res += chr(o)
        elif "a" <= s and s <= "z":
            o = ord(s) + offset
            if o > ord("z"):
                o -= ord("z") - ord("a") + 1
            res += chr(o)
        else:
            res += s

    return res


def main():
    i = input("crypt: ")
    n = int(input("offset: "))
    o = ccyper(i, n)
    print(o)


if __name__ == "__main__":
    main()
