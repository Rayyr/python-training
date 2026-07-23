class student:
    def __init__(self,id,grades,name):
        self.name=name
        self.id=id
        self.grades=grades
    
    def add_grade(self,grade):
        self.grades.append(grade)

    def get_avg(self):
        if not self.grades:
           return 0
        
        sum=0
        for i in self.grades:
            sum+=i
        return sum/len(self.grades)

    def __str__(self):
        return f"{self.name} ({self.id})"

g=[10,10,20]
s=student(1,g,"rya")
print(s.get_avg())
s.add_grade(10)
print(s.get_avg())
print(s)