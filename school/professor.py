class Professor:
    def __init__(self, name):
        self.name = name

    def assign_grade(self, student, grade):
        student.add_grade(grade)
