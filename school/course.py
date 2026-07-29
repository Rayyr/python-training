class Course:
    def __init__(self, name):
        self.name = name
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def __iter__(self):
        return iter(self.students)

    def __len__(self):
        return len(self.students)
