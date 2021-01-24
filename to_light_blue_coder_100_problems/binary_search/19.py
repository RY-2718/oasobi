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


def main():
    total_distance = int(input())
    len_shops = int(input())
    len_orders = int(input())

    shops = [0]
    for i in range(len_shops - 1):
        d = int(input())
        shops.append(d)

    orders = []
    for i in range(len_orders):
        k = int(input())
        orders.append(k)

    shops.sort()

    # print("shops: {}".format(shops))
    # print("orders: {}".format(orders))

    def isOK(arr, value, mid):
        return arr[mid] >= value

    ans = 0

    for order in orders:
        index = binary_search(shops, order, isOK)
        if index == 0:
            left = shops[len_shops - 1] - total_distance
            right = shops[index]
        elif index == len_shops:
            left = shops[index - 1]
            right = shops[0] + total_distance
        else:
            left = shops[index - 1]
            right = shops[index]

        # print("order: {}, left: {}, right: {}".format(order, left, right))

        ans += min(abs(order - left), abs(order - right))

    print(ans)


if __name__ == "__main__":
    main()
