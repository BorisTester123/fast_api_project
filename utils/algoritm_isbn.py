import random

def generate_isbn13() -> str:
    prefix = "978"

    body = "".join(str(random.randint(0, 9)) for _ in range(9))

    partial = prefix + body

    total = 0

    for index, digit in enumerate(partial):
        number = int(digit)

        if index % 2 == 0:
            total += number
        else:
            total += number * 3

    check_digit = (10 - (total % 10)) % 10

    return partial + str(check_digit)