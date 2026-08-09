from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from ..models.course import Course
from ..extensions import db

course_bp = Blueprint("courses", __name__, url_prefix="/courses")

def role_required(*roles):
    def decorator(view):
        from functools import wraps
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_role(*roles):
                flash("You do not have permission to perform that action.", "error")
                return redirect("/courses/")
            return view(*args, **kwargs)
        return wrapped
    return decorator

@course_bp.route("/")
@login_required
def list_courses():
    courses = Course.query.order_by(Course.title.asc()).all()
    return render_template("courses.html", courses=courses)

@course_bp.route("/add", methods=["POST"])
@login_required
@role_required("admin", "instructor")
def add_course():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    if not title:
        flash("Course title is required.", "error")
        return redirect("/courses/")

    db.session.add(Course(title=title, description=description))
    db.session.commit()
    flash("Course added.", "success")
    return redirect("/courses/")
