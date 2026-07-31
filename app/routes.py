from flask import Blueprint, render_template, request, redirect
from .models import Student
from .extensions import db

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return "<h1>Student Portal DB Version</h1>"


@main.route("/students")
def students():
    all_students = Student.query.all()
    return render_template("students.html", students=all_students)


@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        student = Student(
            id=request.form.get("id"),
            name=request.form.get("name"),
            email=request.form.get("email")
        )

        db.session.add(student)
        db.session.commit()

        return redirect("/students")

    return render_template("register.html")