from school import Student, Course

s1 = Student(1, "Alice", [80, 90])
s2 = Student(2, "Bob", [70, 60])

course = Course("Python")
course.add_student(s1)
course.add_student(s2)

for s in course:
    print(s)

print("Total students:", len(course))
