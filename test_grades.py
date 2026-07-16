# test_grades.py

import pytest
from grades import getTop3, validate_students, get_pass_fail


# ✅ Sorting Tests

def test_top3_correct_order():
    students = [
        {"name": "A", "grade": 70},
        {"name": "B", "grade": 95},
        {"name": "C", "grade": 85},
        {"name": "D", "grade": 60},
        {"name": "E", "grade": 90},
    ]

    top3 = getTop3(students)

    assert top3[0]["name"] == "B"
    assert top3[1]["name"] == "E"
    assert top3[2]["name"] == "C"


def test_top3_less_than_three():
    students = [
        {"name": "A", "grade": 80},
        {"name": "B", "grade": 90},
    ]

    top3 = getTop3(students)

    assert len(top3) == 2


# ✅ Validation Tests

def test_validate_students_valid():
    students = [
        {"name": "A", "grade": 50},
        {"name": "B", "grade": 100},
    ]

    assert validate_students(students) is True


def test_validate_students_invalid_negative():
    students = [
        {"name": "A", "grade": -10},
    ]

    assert validate_students(students) is False


def test_validate_students_invalid_over_100():
    students = [
        {"name": "A", "grade": 150},
    ]

    assert validate_students(students) is False


def test_getTop3_raises_error_on_invalid():
    students = [
        {"name": "A", "grade": 90},
        {"name": "B", "grade": -5},
    ]

    with pytest.raises(ValueError):
        getTop3(students)


# ✅ Pass/Fail Tests

def test_pass_fail_conversion():
    students = {
        "A": 80,
        "B": 40,
    }

    result = get_pass_fail(students)

    assert result["A"] == "Pass"
    assert result["B"] == "Fail"


# 🔥 Parametrized Test

@pytest.mark.parametrize("grade,expected", [
    (0, True),
    (50, True),
    (100, True),
    (-1, False),
    (101, False),
])
def test_grade_bounds(grade, expected):
    students = [{"name": "Test", "grade": grade}]
    assert validate_students(students) == expected