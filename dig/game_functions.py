import random


def gen_map() -> str:
    """
    0 - empty
    2 - diamond(? on button)
    """
    s = ["0" for _ in range(15)]
    s[random.randint(0, 14)] = '2'
    return ''.join(s)


def time_for_dig(efficiency_level: int) -> float:
    return (10.0, 8.0, 7.692307692307692, 7.4074074074074066, 7.142857142857143, 6.8965517241379315)[efficiency_level]


def diamonds_number(fortune_level: int) -> int:
    if fortune_level == 1:
        return random.choices([1, 2], [0.6666666666666666, 0.3333333333333333])[0]
    elif fortune_level == 2:
        return random.choices([1, 2, 3], [0.5, 0.25, 0.25])[0]
    elif fortune_level == 3:
        return random.choices([1, 2, 3, 4], [0.4, 0.2, 0.2, 0.2])[0]
    else:
        return 1


def dig_cell(seconds_delta: float, dirt_map: str, dig_index: int,
             efficiency_level: int, fortune_level: int) -> tuple[str, int]:
    """
    :param seconds_delta: Delta in seconds
    :param dirt_map: Players's map
    :param dig_index: Index of dig
    :param efficiency_level: No comments
    :param fortune_level: No comments
    :return: Tuple (new_dirt_map, diamonds_given)
    0 - empty, hide
    1 - empty, open
    2 - diamond(? on button)
    """
    if seconds_delta < time_for_dig(efficiency_level):
        return dirt_map, -1
    elif dirt_map[dig_index] == '1':
        return dirt_map, -2
    if dirt_map[dig_index] == "0":
        return dirt_map[:dig_index] + '1' + dirt_map[dig_index + 1:], 0
    return gen_map(), diamonds_number(fortune_level)


def buy_fortune(fortune_level: int, diamonds_amount: int) -> tuple[bool, int]:
    """
    :param fortune_level: Fortune level on start
    :param diamonds_amount: Amount of diamonds on start
    :return: Tuple (success, new_diamonds_amount)
    """
    if len(FORTUNE_PRICES) - 1 > fortune_level:
        price = FORTUNE_PRICES[fortune_level]
        if diamonds_amount >= price:
            return True, diamonds_amount - price
    return False, diamonds_amount


def buy_efficiency(efficiency_level: int, diamonds_amount: int) -> tuple[bool, int]:
    """
    :param efficiency_level: Fortune level on start
    :param diamonds_amount: Amount of diamonds on start
    :return: Tuple (success, new_diamonds_amount)
    """
    if len(EFFICIENCY_PRICES) - 1 > efficiency_level:
        price = EFFICIENCY_PRICES[efficiency_level]
        if diamonds_amount >= price:
            return True, diamonds_amount - price
    return False, diamonds_amount


EFFICIENCY_PRICES = [3, 3, 5, 7, 7]
FORTUNE_PRICES = [6, 12, 18]

