from Student import student 

class GraduateStudent(student):
    def __init__(self,name,id,grades,thesis):
        super().__init__(id,grades,name)
        self.thesis=thesis
    
    def __str__(self):
           return f"{self.name} ({self.id}) - Thesis: {self.thesis}"