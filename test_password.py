# test_password.py

import pytest
from password_utils import strong_password, WeakPasswordError


def test_valid_password():
    assert strong_password("Strong1!") is True


def test_short_password():
    with pytest.raises(WeakPasswordError):
        strong_password("S1!")


def test_no_uppercase():
    with pytest.raises(WeakPasswordError):
        strong_password("weak1!")


def test_no_number():
    with pytest.raises(WeakPasswordError):
        strong_password("Weak Password!")


def test_no_special_char():
    with pytest.raises(WeakPasswordError):
        strong_password("Weak1234")