class Student:
    def __init__(self, student_id, name, grades=None):
        self.id = student_id
        self.name = name
        self._grades = list(grades) if grades else []

    @property
    def gpa(self):
        if not self._grades:
            return 0
        return sum(self._grades) / len(self._grades)

    def add_grade(self, grade):
        self._grades.append(grade)

    def __eq__(self, other):
        return isinstance(other, Student) and self.id == other.id

    def __str__(self):
        return f"{self.name} ({self.id}) GPA: {self.gpa:.2f}"
