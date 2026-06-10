


def validate_password(password: str) -> str:
    if len(password) < 5:
        raise Exception("Password must be at least 5 characters")

    if password.isnumeric():
        raise Exception("Password must contain numbers and letters")

    if password.isalpha():
        raise Exception("Password must contain numbers and letters")

    if password.isspace():
        raise Exception("Password cannot be only spaces")

    return password

