from flask import Blueprint, flash, redirect, render_template, request, url_for, jsonify
from app import db
from app.forms.course import CourseForm
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.routes.auth import (
    login_required,
    admin_required,
)

courses_bp = Blueprint("courses", __name__)


@courses_bp.route("/courses")
@login_required
def list_courses():
    q = request.args.get("q", "").strip()
    query = Course.query
    if q:
        query = query.filter((Course.code.ilike(f"%{q}%")) | (Course.name.ilike(f"%{q}%")))
    courses = query.order_by(Course.code).paginate(
        page=request.args.get("page", 1, type=int), per_page=5, error_out=False
    )
    return render_template("courses/list.html", courses=courses, q=q)


@courses_bp.route("/courses/new", methods=["GET", "POST"])
@admin_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        if Course.query.filter_by(code=form.code.data).first():
            flash("A course with that code already exists.", "danger")
            return render_template("courses/form.html", form=form, title="Add Course")
        course = Course(
            code=form.code.data.upper(), name=form.name.data, description=form.description.data
        )
        db.session.add(course)
        db.session.commit()
        flash("Course created successfully.", "success")
        return redirect(url_for("courses.list_courses"))
    return render_template("courses/form.html", form=form, title="Add Course")


@courses_bp.route("/courses/<int:course_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        duplicate = Course.query.filter(
            Course.code == form.code.data.upper(), Course.id != course.id
        ).first()
        if duplicate:
            flash("That course code is already in use.", "danger")
            return render_template("courses/form.html", form=form, title="Edit Course")
        course.code = form.code.data.upper()
        course.name = form.name.data
        course.description = form.description.data
        db.session.commit()
        flash("Course updated successfully.", "success")
        return redirect(url_for("courses.list_courses"))
    return render_template("courses/form.html", form=form, title="Edit Course")


@courses_bp.route("/courses/<int:course_id>/delete", methods=["POST"])
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash("Course deleted successfully.", "success")
    return redirect(url_for("courses.list_courses"))


@courses_bp.route("/api/courses")
@login_required
def api_courses():
    return jsonify(
        [
            {"id": c.id, "code": c.code, "name": c.name, "description": c.description}
            for c in Course.query.order_by(Course.code).all()
        ]
    )


@courses_bp.route("/api/courses/<int:course_id>/enrollments", methods=["GET", "POST"])
@login_required
def api_enrollments(course_id):
    course = Course.query.get_or_404(course_id)
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        student_id = data.get("student_id")
        if not student_id:
            return jsonify({"error": "student_id is required"}), 400
        if Enrollment.query.filter_by(student_id=student_id, course_id=course.id).first():
            return jsonify({"error": "Already enrolled"}), 409
        enrollment = Enrollment(student_id=student_id, course_id=course.id)
        db.session.add(enrollment)
        db.session.commit()
        return jsonify({"message": "Enrollment created", "id": enrollment.id}), 201

    return jsonify(
        [
            {"id": e.student.id, "name": e.student.name, "email": e.student.email}
            for e in course.enrollments
        ]
    )
