# password_utils.py

import re


class WeakPasswordError(Exception):
    pass


def strong_password(password: str) -> bool:
    if len(password) < 8:
        raise WeakPasswordError("Password must be at least 8 characters")

    if not any(c.isupper() for c in password):
        raise WeakPasswordError("Must include uppercase letter")

    if not any(c.isdigit() for c in password):
        raise WeakPasswordError("Must include a number")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise WeakPasswordError("Must include a special character")

    return True