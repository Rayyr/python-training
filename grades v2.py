def validate_students(students):
 
    for s in students:
        if not (0 <= s["grade"] <= 100):
            return False
    return True


def getTop3(students_list):
 
    if not validate_students(students_list):
        raise ValueError("Invalid grades detected")

    return sorted(students_list, key=lambda s: s["grade"], reverse=True)[:3]


def get_pass_fail(students_dict, pass_mark=50):
 
    return {
        name: ("Pass" if grade >= pass_mark else "Fail")
        for name, grade in students_dict.items()
    }


def main():
    students_list = [
        {"name": "Alice", "grade": 88},
        {"name": "Bob", "grade": 45},
        {"name": "Charlie", "grade": 72},
        {"name": "David", "grade": 30},
        {"name": "Eve", "grade": 95},
    ]

    # Convert list to dict
    students_dict = {s["name"]: s["grade"] for s in students_list}

    # Top 3
    top3 = getTop3(students_list)

    # Pass/Fail
    pass_fail = get_pass_fail(students_dict)
 
    for i, s in enumerate(top3, start=1):
        print(f"{i}. {s['name']} - {s['grade']}")

   
    for name, status in pass_fail.items():
        print(f"{name}: {status}")
   


if __name__ == "__main__":
    main()