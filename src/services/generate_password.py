import random
import string


def generate_password():
    """
    The generate_password function generates a random password consisting of a letter, a digit,
    and a combination of letters and digits.

    :return: A string of length 8
    """
    letter = random.choice(string.ascii_letters)
    digit = random.choice(string.digits)
    symbols = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    password = letter + digit + symbols
    password = ''.join(random.sample(password, len(password)))
    return password

