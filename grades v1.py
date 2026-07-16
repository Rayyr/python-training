def getTop3(students):
     ss=sorted(students, key=lambda s: s["grade"],reverse=True)
     return ss[:3]


def main():
    students=[
        {"name": "s1", "grade": 88},
        {"name": "s2", "grade": 95},
        {"name": "s3", "grade": 90},
        {"name": "s4", "grade": 85},
        {"name": "s5", "grade": 92},
    ]


    top3=getTop3(students)
  
    for i, student in enumerate(top3, start=1):
       print(f"{i}. {student['name']} - {student['grade']}")

if __name__=="__main__":
  main()