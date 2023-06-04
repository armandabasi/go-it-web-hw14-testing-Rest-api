import string

from src.services.generate_password import generate_password


def test_generate_password():
    password = generate_password()
    assert isinstance(password, str)
    assert len(password) == 8

    has_letter = any(char.isalpha() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_symbols = any(char in string.ascii_letters + string.digits for char in password)

    assert has_letter
    assert has_digit
    assert has_symbols
