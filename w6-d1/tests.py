import pytest
from stu_class import student    


def test_initialization():
    s = student(1, [10, 20], "Riya")
    assert s.id == 1
    assert s.name == "Riya"
    assert s.grades == [10, 20]


def test_add_grade():
    s = student(1, [10], "Riya")
    s.add_grade(20)
    assert s.grades == [10, 20]


def test_get_avg_basic():
    s = student(1, [10, 20, 30], "Riya")
    assert s.get_avg() == 20


def test_get_avg_after_adding_grade():
    s = student(1, [10, 20], "Riya")
    s.add_grade(30)
    assert s.get_avg() == 20


def test_string_representation():
    s = student(1, [10], "Riya")
    assert str(s) == "Riya (1)"