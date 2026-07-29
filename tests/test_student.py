from school import Student

def test_gpa():
    s = Student(1, "Alice", [80, 90])
    assert s.gpa == 85
