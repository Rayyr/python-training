# students/manager.py

from .models import Student
from .utils import load_data, save_data


class StudentManager:
    def __init__(self):
        self.students = [Student.from_dict(s) for s in load_data()]

    def add_student(self, name, student_id, email):
        if any(s.student_id == student_id for s in self.students):
            raise ValueError("Student ID already exists")

        student = Student(name, student_id, email)
        self.students.append(student)
        self._save()

    def update_grades(self, student_id, grades):
        student = self._find(student_id)
        student.grades = grades
        self._save()

    def top_students(self, n=3):
        return sorted(self.students, key=lambda s: s.average(), reverse=True)[:n]

    def list_students(self):
        return self.students

    def _find(self, student_id):
        for s in self.students:
            if s.student_id == student_id:
                return s
        raise ValueError("Student not found")

    def _save(self):
        save_data([s.to_dict() for s in self.students])
