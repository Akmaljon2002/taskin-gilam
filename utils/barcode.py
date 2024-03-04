import random


def generate_unique_number():
    unique_numbers = ''
    for i in range(0, 14):
        number = random.randint(0, 9)
        unique_numbers += str(number) + '.'

    return unique_numbers.replace('.', '')