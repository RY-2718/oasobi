def main():
    n = int(input())
    heights = []

    lasts = []

    for i in range(n):
        height = []
        h, s = map(int, input().split(" "))
        for j in range(n):
            height.append(h + s * j)

        lasts.append(h + s * (n - 1))

        heights.append(height)

    lasts.sort()

    def gt(arr, value, mid):
        return arr[mid] > value

    for i in range(n):
        last = lasts[i]
        shots = list(range(n - 1))
        shootable = True

        # print("last: {}".format(last))

        for j in range(n):
            if j == i:
                continue

            # print("\twill find index which is lt {} from {}".format(last, heights[j]))
            deadline = binary_search(heights[j], last, gt) - 1
            # print("\tdeadline[{}]: {}".format(j, deadline))
            if deadline == -1:
                shootable = False
                continue

            when = binary_search(shots, deadline, gt) - 1
            if when == -1:
                shootable = False
                continue
            shots.pop(when)
            # print("\tshoot at {}".format(when))
            # print("\tremained shots: {}".format(shots))

        if shootable:
            print(last)
            return


def binary_search(arr, value, isOK):
    ng = -1
    ok = len(arr)

    while abs(ok - ng) > 1:
        mid = ng + (ok - ng) // 2

        if isOK(arr, value, mid):
            ok = mid
        else:
            ng = mid

    return ok


if __name__ == "__main__":
    main()
