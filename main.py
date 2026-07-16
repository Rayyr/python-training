# main.py

from students.manager import StudentManager
from students.utils import export_csv


def main():
    sm = StudentManager()

    while True:
        print("\nStudent Management System")
        print("1. Add Student")
        print("2. Update Grades")
        print("3. Show Top Students")
        print("4. Export CSV")
        print("5. Exit")

        choice = input("Choose: ")

        try:
            if choice == "1":
                name = input("Name: ")
                sid = input("ID: ")
                email = input("Email: ")
                sm.add_student(name, sid, email)

            elif choice == "2":
                sid = input("ID: ")
                grades = list(map(int, input("Grades (space-separated): ").split()))
                sm.update_grades(sid, grades)

            elif choice == "3":
                for s in sm.top_students():
                    print(f"{s.name} → {s.average():.2f}")

            elif choice == "4":
                export_csv([s.to_dict() for s in sm.list_students()])
                print("Exported!")

            elif choice == "5":
                break

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
