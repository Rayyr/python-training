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

    # Optional: average GPA
    def average_gpa(self):
        if not self.students:
            return 0
        return sum(s.gpa for s in self.students) / len(self.students)