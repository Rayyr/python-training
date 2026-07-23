class Professor:
    def __init__(self,name):
        self.name=name
    
    def assign_grade(self,grade,student_obj):
        student_obj.add_grade(grade)