from flask import Blueprint, render_template, request, redirect
from .models import add_student, get_students, get_student

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("index.html")


@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        student = {
            "name": request.form.get("name"),
            "id": request.form.get("id"),
            "email": request.form.get("email"),
            "grades": []
        }
        add_student(student)
        return redirect("/students")

    return render_template("register.html")


@main.route("/students")
def students():
    return render_template("students.html", students=get_students())


@main.route("/student/<student_id>")
def student_detail(student_id):
    student = get_student(student_id)
    return render_template("student_detail.html", student=student)