# tests/test_students.py
import sys
import os
import pytest


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from students.manager import StudentManager


def setup_function():
    if os.path.exists("data/students.json"):
        os.remove("data/students.json")


def test_add_student():
    sm = StudentManager()
    sm.add_student("Alice", "1", "a@mail.com")

    assert len(sm.list_students()) == 1


def test_duplicate_id():
    sm = StudentManager()
    sm.add_student("A", "1", "a@mail.com")

    with pytest.raises(ValueError):
        sm.add_student("B", "1", "b@mail.com")


def test_update_grades():
    sm = StudentManager()
    sm.add_student("A", "1", "a@mail.com")
    sm.update_grades("1", [90, 100])

    assert sm.list_students()[0].grades == [90, 100]


def test_top_students():
    sm = StudentManager()
    sm.add_student("A", "1", "a@mail.com")
    sm.add_student("B", "2", "b@mail.com")

    sm.update_grades("1", [50])
    sm.update_grades("2", [90])

    top = sm.top_students()
    assert top[0].name == "B"


def test_student_not_found():
    sm = StudentManager()

    with pytest.raises(ValueError):
        sm.update_grades("999", [100])
