import os
import uuid
from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from sqlalchemy import or_
from werkzeug.utils import secure_filename
from app import db
from app.forms.student import StudentForm
from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.routes.auth import login_required

students_bp = Blueprint("students", __name__)


@students_bp.route("/")
def index():
    return redirect(url_for("students.list_students"))


@students_bp.route("/students")
@login_required
def list_students():
    q = request.args.get("q", "").strip()
    query = Student.query
    if q:
        query = query.filter(or_(Student.name.ilike(f"%{q}%"), Student.email.ilike(f"%{q}%")))
    students = query.order_by(Student.name).paginate(
        page=request.args.get("page", 1, type=int), per_page=5, error_out=False
    )
    return render_template("students/list.html", students=students, q=q)


@students_bp.route("/students/new", methods=["GET", "POST"])
@login_required
def create_student():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(name=form.name.data, email=form.email.data, phone=form.phone.data)
        if Student.query.filter_by(email=form.email.data).first():
            flash("A student with this email already exists.", "danger")
            return render_template("students/form.html", form=form, title="Add Student")

        if form.profile_picture.data:
            filename = secure_filename(form.profile_picture.data.filename)
            filename = f"{uuid.uuid4().hex}_{filename}"
            form.profile_picture.data.save(
                os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            )
            student.profile_picture = filename

        db.session.add(student)
        db.session.commit()
        flash("Student created successfully.", "success")
        return redirect(url_for("students.list_students"))
    return render_template("students/form.html", form=form, title="Add Student")


@students_bp.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        duplicate = Student.query.filter(
            Student.email == form.email.data, Student.id != student.id
        ).first()
        if duplicate:
            flash("That email is already in use.", "danger")
            return render_template("students/form.html", form=form, title="Edit Student")

        student.name = form.name.data
        student.email = form.email.data
        student.phone = form.phone.data

        if form.profile_picture.data:
            filename = secure_filename(form.profile_picture.data.filename)
            filename = f"{uuid.uuid4().hex}_{filename}"
            form.profile_picture.data.save(
                os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            )
            student.profile_picture = filename

        db.session.commit()
        flash("Student updated successfully.", "success")
        return redirect(url_for("students.detail_student", student_id=student.id))
    return render_template("students/form.html", form=form, title="Edit Student")


@students_bp.route("/students/<int:student_id>")
@login_required
def detail_student(student_id):
    student = Student.query.get_or_404(student_id)
    courses = Course.query.join(Enrollment).filter(Enrollment.student_id == student.id).all()
    return render_template(
        "students/detail.html",
        student=student,
        courses=courses,
        all_courses=Course.query.order_by(Course.code).all(),
    )


@students_bp.route("/students/<int:student_id>/delete", methods=["POST"])
@login_required
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash("Student deleted successfully.", "success")
    return redirect(url_for("students.list_students"))


@students_bp.route("/students/<int:student_id>/enroll", methods=["POST"])
@login_required
def enroll_student(student_id):
    student = Student.query.get_or_404(student_id)
    course = Course.query.get_or_404(request.form.get("course_id", type=int))
    if Enrollment.query.filter_by(student_id=student.id, course_id=course.id).first():
        flash("Student is already enrolled in this course.", "warning")
    else:
        db.session.add(Enrollment(student_id=student.id, course_id=course.id))
        db.session.commit()
        flash("Enrollment added.", "success")
    return redirect(url_for("students.detail_student", student_id=student.id))


@students_bp.route("/students/<int:student_id>/unenroll/<int:course_id>", methods=["POST"])
@login_required
def unenroll_student(student_id, course_id):
    enrollment = Enrollment.query.filter_by(
        student_id=student_id, course_id=course_id
    ).first_or_404()
    db.session.delete(enrollment)
    db.session.commit()
    flash("Enrollment removed.", "success")
    return redirect(url_for("students.detail_student", student_id=student_id))


@students_bp.route("/api/students")
@login_required
def api_students():
    q = request.args.get("q", "").strip()
    query = Student.query
    if q:
        query = query.filter(or_(Student.name.ilike(f"%{q}%"), Student.email.ilike(f"%{q}%")))
    return jsonify(
        [
            {"id": s.id, "name": s.name, "email": s.email, "phone": s.phone}
            for s in query.order_by(Student.name).limit(50).all()
        ]
    )


@students_bp.route("/api/students/<int:student_id>", methods=["GET", "PUT", "DELETE"])
@login_required
def api_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == "GET":
        return jsonify(
            {
                "id": student.id,
                "name": student.name,
                "email": student.email,
                "phone": student.phone,
                "courses": [{"id": c.id, "code": c.code, "name": c.name} for c in student.courses],
            }
        )
    if request.method == "DELETE":
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Student deleted"})
    data = request.get_json(silent=True) or {}
    student.name = data.get("name", student.name)
    student.email = data.get("email", student.email)
    student.phone = data.get("phone", student.phone)
    db.session.commit()
    return jsonify({"message": "Student updated", "id": student.id})
