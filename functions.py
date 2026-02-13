


def check_input(money: int) -> int:
    for i in money:
        if i.isalpha():
            return 400
    return 200