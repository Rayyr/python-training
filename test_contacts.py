# test_contacts.py

import os
from contacts.manager import ContactManager


def setup_function():
    # clean file before each test
    if os.path.exists("contacts.json"):
        os.remove("contacts.json")


def test_add_and_search():
    cm = ContactManager()
    cm.add_contact("Alice", "123", "a@mail.com")

    result = cm.search_by_name("Alice")

    assert result["phone"] == "123"
    assert result["email"] == "a@mail.com"


def test_search_by_phone():
    cm = ContactManager()
    cm.add_contact("Bob", "999", "b@mail.com")

    result = cm.search_by_phone("999")

    assert result[0] == "Bob"


def test_not_found():
    cm = ContactManager()
    assert cm.search_by_name("Unknown") is None