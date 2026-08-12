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
    session,
    url_for,
)

from sqlalchemy import or_
from werkzeug.utils import secure_filename

from app import db
from app.forms.student import StudentForm
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.student import Student
from app.models.user import User
from app.routes.auth import admin_required, login_required

students_bp = Blueprint("students", __name__)


# ============================================================
# HOME
# ============================================================


@students_bp.route("/")
def index():
    return redirect(url_for("students.profile"))


# ============================================================
# ADMIN: LIST STUDENTS
# ============================================================


@students_bp.route("/students")
@admin_required
def list_students():

    q = request.args.get("q", "").strip()

    query = Student.query

    if q:
        query = query.filter(
            or_(
                Student.name.ilike(f"%{q}%"),
                Student.email.ilike(f"%{q}%"),
            )
        )

    students = query.order_by(Student.name).paginate(
        page=request.args.get(
            "page",
            1,
            type=int,
        ),
        per_page=5,
        error_out=False,
    )

    return render_template(
        "students/list.html",
        students=students,
        q=q,
    )


# ============================================================
# ADMIN: CREATE STUDENT
# ============================================================


@students_bp.route(
    "/students/new",
    methods=["GET", "POST"],
)
@admin_required
def create_student():

    form = StudentForm()

    if form.validate_on_submit():

        email = form.email.data.strip().lower()

        # Check duplicate student
        if Student.query.filter_by(email=email).first():

            flash(
                "A student with this email already exists.",
                "danger",
            )

            return render_template(
                "students/form.html",
                form=form,
                title="Add Student",
            )

        # Check duplicate user
        if User.query.filter_by(email=email).first():

            flash(
                "A user account with this email already exists.",
                "danger",
            )

            return render_template(
                "students/form.html",
                form=form,
                title="Add Student",
            )

        # Create student
        student = Student(
            name=form.name.data,
            email=email,
            phone=form.phone.data,
        )

        # Profile picture
        if form.profile_picture.data:

            filename = secure_filename(form.profile_picture.data.filename)

            filename = f"{uuid.uuid4().hex}_{filename}"

            upload_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename,
            )

            form.profile_picture.data.save(upload_path)

            student.profile_picture = filename

        db.session.add(student)
        db.session.flush()

        # ----------------------------------------------------
        # Create login account for the student
        # ----------------------------------------------------

        user = User(
            name=student.name,
            email=student.email,
            role="student",
            student_id=student.id,
        )

        # Temporary default password.
        # Ideally change this to a generated password
        # or password-reset system later.
        user.set_password("student123")

        db.session.add(user)
        db.session.commit()

        flash(
            "Student and login account created successfully.",
            "success",
        )

        return redirect(url_for("students.list_students"))

    return render_template(
        "students/form.html",
        form=form,
        title="Add Student",
    )


# ============================================================
# ADMIN: EDIT ANY STUDENT
# ============================================================


@students_bp.route(
    "/students/<int:student_id>/edit",
    methods=["GET", "POST"],
)
@admin_required
def edit_student(student_id):

    student = Student.query.get_or_404(student_id)

    form = StudentForm(obj=student)

    if form.validate_on_submit():

        email = form.email.data.strip().lower()

        duplicate = Student.query.filter(
            Student.email == email,
            Student.id != student.id,
        ).first()

        if duplicate:

            flash(
                "That email is already in use.",
                "danger",
            )

            return render_template(
                "students/form.html",
                form=form,
                title="Edit Student",
            )

        student.name = form.name.data
        student.email = email
        student.phone = form.phone.data

        if form.profile_picture.data:

            filename = secure_filename(form.profile_picture.data.filename)

            filename = f"{uuid.uuid4().hex}_{filename}"

            form.profile_picture.data.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    filename,
                )
            )

            student.profile_picture = filename

        # Keep login account synchronized
        user = User.query.filter_by(student_id=student.id).first()

        if user:

            user.name = student.name
            user.email = student.email

        db.session.commit()

        flash(
            "Student updated successfully.",
            "success",
        )

        return redirect(
            url_for(
                "students.detail_student",
                student_id=student.id,
            )
        )

    return render_template(
        "students/form.html",
        form=form,
        title="Edit Student",
    )


# ============================================================
# VIEW STUDENT
# ADMIN: ANY STUDENT
# STUDENT: ONLY THEMSELVES
# ============================================================


@students_bp.route("/students/<int:student_id>")
@login_required
def detail_student(student_id):

    user = db.session.get(
        User,
        session["user_id"],
    )

    if not user:
        session.clear()

        return redirect(url_for("auth.login"))

    student = Student.query.get_or_404(student_id)

    # Normal students may only see themselves.
    if user.is_student:

        if not user.student or user.student.id != student.id:

            flash(
                "You can only view your own profile.",
                "danger",
            )

            return redirect(url_for("students.profile"))

    courses = Course.query.join(Enrollment).filter(Enrollment.student_id == student.id).all()

    return render_template(
        "students/detail.html",
        student=student,
        courses=courses,
        all_courses=Course.query.order_by(Course.code).all(),
    )


# ============================================================
# ADMIN: DELETE STUDENT
# ============================================================


@students_bp.route(
    "/students/<int:student_id>/delete",
    methods=["POST"],
)
@admin_required
def delete_student(student_id):

    student = Student.query.get_or_404(student_id)

    # Delete linked user account too.
    user = User.query.filter_by(student_id=student.id).first()

    if user:
        db.session.delete(user)

    db.session.delete(student)
    db.session.commit()

    flash(
        "Student deleted successfully.",
        "success",
    )

    return redirect(url_for("students.list_students"))


# ============================================================
# ENROLL CURRENT STUDENT
# ============================================================


@students_bp.route(
    "/courses/<int:course_id>/enroll",
    methods=["POST"],
)
@login_required
def enroll_current_student(course_id):

    user = db.session.get(
        User,
        session["user_id"],
    )

    if not user:

        session.clear()

        return redirect(url_for("auth.login"))

    course = Course.query.get_or_404(course_id)

    # --------------------------------------------------------
    # ADMIN
    # --------------------------------------------------------

    if user.is_admin:

        student_id = request.form.get(
            "student_id",
            type=int,
        )

        if not student_id:

            flash(
                "Student ID is required.",
                "danger",
            )

            return redirect(url_for("courses.list_courses"))

        student = Student.query.get_or_404(student_id)

    # --------------------------------------------------------
    # NORMAL STUDENT
    # --------------------------------------------------------

    else:

        if not user.student:

            flash(
                "Your account is not linked to a student profile.",
                "danger",
            )

            return redirect(url_for("students.profile"))

        student = user.student

    # --------------------------------------------------------
    # CHECK DUPLICATE
    # --------------------------------------------------------

    existing = Enrollment.query.filter_by(
        student_id=student.id,
        course_id=course.id,
    ).first()

    if existing:

        flash(
            "This student is already enrolled in this course.",
            "warning",
        )

    else:

        enrollment = Enrollment(
            student_id=student.id,
            course_id=course.id,
        )

        db.session.add(enrollment)
        db.session.commit()

        flash(
            f"{student.name} is now enrolled in {course.name}.",
            "success",
        )

    # Admin goes to student detail
    if user.is_admin:

        return redirect(
            url_for(
                "students.detail_student",
                student_id=student.id,
            )
        )

    # Student goes to own profile
    return redirect(url_for("students.profile"))


# ============================================================
# UNENROLL CURRENT STUDENT
# ============================================================


@students_bp.route(
    "/courses/<int:course_id>/unenroll",
    methods=["POST"],
)
@login_required
def unenroll_current_student(course_id):

    user = db.session.get(
        User,
        session["user_id"],
    )

    if not user or not user.student:

        flash(
            "Student profile not found.",
            "danger",
        )

        return redirect(url_for("students.profile"))

    enrollment = Enrollment.query.filter_by(
        student_id=user.student.id,
        course_id=course_id,
    ).first()

    if not enrollment:

        flash(
            "You are not enrolled in this course.",
            "warning",
        )

        return redirect(url_for("students.profile"))

    db.session.delete(enrollment)
    db.session.commit()

    flash(
        "You have been unenrolled from the course.",
        "success",
    )

    return redirect(url_for("students.profile"))


# ============================================================
# ADMIN: REMOVE ENROLLMENT
# ============================================================


@students_bp.route(
    "/students/<int:student_id>/unenroll/<int:course_id>",
    methods=["POST"],
)
@admin_required
def admin_unenroll_student(
    student_id,
    course_id,
):

    enrollment = Enrollment.query.filter_by(
        student_id=student_id,
        course_id=course_id,
    ).first_or_404()

    db.session.delete(enrollment)
    db.session.commit()

    flash(
        "Enrollment removed.",
        "success",
    )

    return redirect(
        url_for(
            "students.detail_student",
            student_id=student_id,
        )
    )


# ============================================================
# STUDENT PROFILE
# ============================================================


@students_bp.route("/profile")
@login_required
def profile():

    user = db.session.get(
        User,
        session["user_id"],
    )

    if not user:

        session.clear()

        return redirect(url_for("auth.login"))

    # Admin doesn't have a Student profile.
    if user.is_admin:

        return redirect(url_for("students.list_students"))

    student = user.student

    if not student:

        flash(
            "Your account is not linked to a student profile.",
            "danger",
        )

        return redirect(url_for("auth.login"))

    courses = (
        Course.query.join(Enrollment)
        .filter(Enrollment.student_id == student.id)
        .order_by(Course.code)
        .all()
    )

    return render_template(
        "students/profile.html",
        student=student,
        courses=courses,
    )


# ============================================================
# STUDENT: EDIT OWN PROFILE
# ============================================================


@students_bp.route(
    "/profile/edit",
    methods=["GET", "POST"],
)
@login_required
def edit_profile():

    user = db.session.get(
        User,
        session["user_id"],
    )

    if not user:

        session.clear()

        return redirect(url_for("auth.login"))

    if user.is_admin:

        flash(
            "Administrators should use the admin tools.",
            "info",
        )

        return redirect(url_for("students.list_students"))

    student = user.student

    if not student:

        flash(
            "Student profile not found.",
            "danger",
        )

        return redirect(url_for("auth.login"))

    form = StudentForm(obj=student)

    if form.validate_on_submit():

        email = form.email.data.strip().lower()

        duplicate = Student.query.filter(
            Student.email == email,
            Student.id != student.id,
        ).first()

        if duplicate:

            flash(
                "That email is already in use.",
                "danger",
            )

            return render_template(
                "students/form.html",
                form=form,
                title="Edit My Profile",
            )

        student.name = form.name.data
        student.email = email
        student.phone = form.phone.data

        if form.profile_picture.data:

            filename = secure_filename(form.profile_picture.data.filename)

            filename = f"{uuid.uuid4().hex}_{filename}"

            form.profile_picture.data.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    filename,
                )
            )

            student.profile_picture = filename

        # Synchronize login account
        user.name = student.name
        user.email = student.email

        db.session.commit()

        flash(
            "Your profile was updated successfully.",
            "success",
        )

        return redirect(url_for("students.profile"))

    return render_template(
        "students/form.html",
        form=form,
        title="Edit My Profile",
    )


# ============================================================
# ADMIN: STUDENT API
# ============================================================


@students_bp.route("/api/students")
@admin_required
def api_students():

    q = request.args.get(
        "q",
        "",
    ).strip()

    query = Student.query

    if q:

        query = query.filter(
            or_(
                Student.name.ilike(f"%{q}%"),
                Student.email.ilike(f"%{q}%"),
            )
        )

    return jsonify(
        [
            {
                "id": student.id,
                "name": student.name,
                "email": student.email,
                "phone": student.phone,
            }
            for student in query.order_by(Student.name).limit(50).all()
        ]
    )


# ============================================================
# ADMIN: SINGLE STUDENT API
# ============================================================


@students_bp.route(
    "/api/students/<int:student_id>",
    methods=["GET", "PUT", "DELETE"],
)
@admin_required
def api_student(student_id):

    student = Student.query.get_or_404(student_id)

    # GET
    if request.method == "GET":

        return jsonify(
            {
                "id": student.id,
                "name": student.name,
                "email": student.email,
                "phone": student.phone,
                "courses": [
                    {
                        "id": course.id,
                        "code": course.code,
                        "name": course.name,
                    }
                    for course in student.courses
                ],
            }
        )

    # DELETE
    if request.method == "DELETE":

        user = User.query.filter_by(student_id=student.id).first()

        if user:
            db.session.delete(user)

        db.session.delete(student)
        db.session.commit()

        return jsonify({"message": "Student deleted"})

    # PUT
    data = request.get_json(silent=True) or {}

    email = data.get(
        "email",
        student.email,
    )

    duplicate = Student.query.filter(
        Student.email == email,
        Student.id != student.id,
    ).first()

    if duplicate:

        return jsonify({"error": "Email already in use"}), 400

    student.name = data.get(
        "name",
        student.name,
    )

    student.email = email

    student.phone = data.get(
        "phone",
        student.phone,
    )

    user = User.query.filter_by(student_id=student.id).first()

    if user:

        user.name = student.name
        user.email = student.email

    db.session.commit()

    return jsonify(
        {
            "message": "Student updated",
            "id": student.id,
        }
    )
