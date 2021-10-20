"""
change in recursion
"""

coins = [1, 3, 5, 10, 20, 50, 100, 3, 9, 15, 30, 60, 150, 300]


def change_cub_recursion(cuc):
    if cuc == 0:
        return 1
    if cuc < 0:
        return 0
    counter = 0
    for coin in coins:
        counter += change_cub_recursion(cuc - coin)
    return counter


a = 20
print(change_cub_recursion(3 * a))
