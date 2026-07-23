class Student:
    def __init__(self, student_id, name, grades=None):
        self.id = student_id
        self.name = name
        self._grades = list(grades) if grades else []

    #  PROPERTY (GPA auto-calculated)
    @property
    def gpa(self):
        if not self._grades:
            return 0
        return sum(self._grades) / len(self._grades)

    #  Optional setter (controlled update)
    @gpa.setter
    def gpa(self, value):
        raise AttributeError("GPA is read-only")

    
    def add_grade(self, grade):
        self._grades.append(grade)

    #  (__eq__)
    def __eq__(self, other):
        if not isinstance(other, Student):
            return False
        return self.id == other.id

    #  STRING
    def __str__(self):
        return f"{self.name} ({self.id}) GPA: {self.gpa:.2f}"

    #  CLASS METHOD
    @classmethod
    def from_string(cls, data_str):
        # "1,Alice,90,80,70"
        parts = data_str.split(",")
        student_id = int(parts[0])
        name = parts[1]
        grades = list(map(int, parts[2:]))
        return cls(student_id, name, grades)

    #  STATIC METHOD
    @staticmethod
    def is_passing(grade):
        return grade >= 40