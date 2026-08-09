from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from sqlalchemy import or_
from ..models.student import Student
from ..models.user import User
from ..extensions import db

student_bp = Blueprint("students", __name__, url_prefix="/students")

def role_required(*roles):
    def decorator(view):
        from functools import wraps
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_role(*roles):
                flash("You do not have permission to perform that action.", "error")
                return redirect("/students/")
            return view(*args, **kwargs)
        return wrapped
    return decorator

@student_bp.route("/")
@login_required
def list_students():
    q = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    per_page = min(max(per_page, 1), 50)

    query = Student.query
    if q:
        query = query.filter(or_(Student.name.ilike(f"%{q}%"),
                                 Student.email.ilike(f"%{q}%")))

    pagination = query.order_by(Student.name.asc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template(
        "students.html",
        students=pagination.items,
        pagination=pagination,
        q=q,
        per_page=per_page,
    )

@student_bp.route("/add", methods=["POST"])
@login_required
@role_required("admin", "instructor")
def add_student():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    if not name or not email:
        flash("Name and email are required.", "error")
        return redirect("/students/")

    if Student.query.filter_by(email=email).first():
        flash("A student with that email already exists.", "error")
        return redirect("/students/")

    student = Student(name=name, email=email)
    db.session.add(student)
    db.session.commit()
    flash("Student added.", "success")
    return redirect("/students/")
