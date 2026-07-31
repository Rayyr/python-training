students = []

def add_student(data):
    students.append(data)

def get_students():
    return students

def get_student(student_id):
    return next((s for s in students if s["id"] == student_id), None)