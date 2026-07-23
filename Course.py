class Course:
    def __init__(self,name):
        self.name=name
        self.students=[]

    def add_student(self,student_obj):
        self.students.append(student_obj)

    def class_avg(self):
        if not self.students
           return 0
        
         return sum(s.get_avg() for s in self.students) / len(self.students) 