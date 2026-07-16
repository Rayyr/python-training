# students/models.py

class Student:
    def __init__(self, name, student_id, email, grades=None):
        self.name = name
        self.student_id = student_id
        self.email = email
        self.grades = grades or []

    def average(self):
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)

    def to_dict(self):
        return {
            "name": self.name,
            "student_id": self.student_id,
            "email": self.email,
            "grades": self.grades
        }

    @staticmethod
    def from_dict(data):
        return Student(
            data["name"],
            data["student_id"],
            data["email"],
            data.get("grades", [])
        )
