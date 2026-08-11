from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from ..models.student import Student
from ..extensions import db


student_bp = Blueprint(
    "students",
    __name__,
    url_prefix="/students"
)


@student_bp.route("/")
def list_students():
    search = request.args.get(
        "search",
        ""
    ).strip()

    page = request.args.get(
        "page",
        1,
        type=int
    )

    query = Student.query

    if search:
        query = query.filter(
            Student.name.ilike(
                f"%{search}%"
            )
        )

    students = query.paginate(
        page=page,
        per_page=5,
        error_out=False
    )

    return render_template(
        "students.html",
        students=students,
        search=search
    )


@student_bp.route("/add", methods=["POST"])
def add_student():
    name = request.form.get(
        "name",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip()

    if not name or not email:
        flash(
            "Name and email are required.",
            "danger"
        )
        return redirect(
            url_for("students.list_students")
        )

    if Student.query.filter_by(
        email=email
    ).first():
        flash(
            "A student with this email already exists.",
            "danger"
        )
        return redirect(
            url_for("students.list_students")
        )

    student = Student(
        name=name,
        email=email
    )

    db.session.add(student)
    db.session.commit()

    flash(
        "Student added successfully!",
        "success"
    )

    return redirect(
        url_for("students.list_students")
    )
