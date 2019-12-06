points = [[1, 1], [1, 1]]


def game(hand_bot, hand_top, player):
    global points

    points[not player][hand_top] = points[not player][hand_top] + points[player][hand_bot]
    points[not player][hand_top] = points[not player][hand_top] % 5


def switch_display_calc(hand_from, hand_to, player):
    amounts = list(range(1, points[player][hand_from] + 1))
    for x in amounts:
        if (x + points[player][hand_to]) >= 5:
            amounts.remove(x)
    if points[player][hand_from] > points[player][hand_to]:
        amounts.remove(points[player][hand_from] - points[player][hand_to])
    return amounts


def switch(amount, hand_from, hand_to, player):
    # if (amount+points[player][hand_to])>5 or amount>points[player][hand_from]:
    #     print('no')
    #     return 0
    # else:
    print('yes')
    points[player][hand_to] = amount + points[player][hand_to]
    points[player][hand_to] = points[player][hand_to] % 5
    points[player][hand_from] = points[player][hand_from] - amount
