from functools import wraps

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app import db
from app.models.user import User
from app.models.student import Student

auth_bp = Blueprint("auth", __name__)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash(
                "Please log in to continue.",
                "warning",
            )
            return redirect(
                url_for(
                    "auth.login",
                    next=request.path,
                )
            )

        return view(*args, **kwargs)

    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash(
                "Please log in to continue.",
                "warning",
            )
            return redirect(
                url_for(
                    "auth.login",
                    next=request.path,
                )
            )

        user = db.session.get(
            User,
            session["user_id"],
        )

        if not user or not user.is_admin:
            flash(
                "Administrator access is required.",
                "danger",
            )
            return redirect(url_for("students.profile"))

        return view(*args, **kwargs)

    return wrapped


def student_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash(
                "Please log in to continue.",
                "warning",
            )
            return redirect(
                url_for(
                    "auth.login",
                    next=request.path,
                )
            )

        user = db.session.get(
            User,
            session["user_id"],
        )

        if not user or not user.is_student:
            flash(
                "Student access is required.",
                "danger",
            )
            return redirect(url_for("students.profile"))

        return view(*args, **kwargs)

    return wrapped


@auth_bp.app_context_processor
def inject_current_user():
    user = None

    if session.get("user_id"):
        user = db.session.get(
            User,
            session["user_id"],
        )

    return {
        "current_user": user,
    }


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():

    if session.get("user_id"):
        return redirect(url_for("students.profile"))

    if request.method == "POST":

        name = request.form.get(
            "name",
            "",
        ).strip()

        email = (
            request.form.get(
                "email",
                "",
            )
            .strip()
            .lower()
        )

        password = request.form.get(
            "password",
            "",
        )

        confirm = request.form.get(
            "confirm_password",
            "",
        )

        if not name or not email or not password:
            flash(
                "All fields are required.",
                "danger",
            )

        elif len(password) < 6:
            flash(
                "Password must be at least 6 characters.",
                "danger",
            )

        elif password != confirm:
            flash(
                "Passwords do not match.",
                "danger",
            )

        elif User.query.filter_by(email=email).first():
            flash(
                "An account with that email already exists.",
                "danger",
            )

        elif Student.query.filter_by(email=email).first():
            flash(
                "A student with that email already exists.",
                "danger",
            )

        else:

            # Create Student first.
            student = Student(
                name=name,
                email=email,
            )

            db.session.add(student)
            db.session.flush()

            # Normal signup is ALWAYS a student.
            user = User(
                name=name,
                email=email,
                role="student",
                student_id=student.id,
            )

            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            session.clear()
            session["user_id"] = user.id

            flash(
                "Account created successfully. Welcome!",
                "success",
            )

            return redirect(url_for("students.profile"))

    return render_template("auth/signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if session.get("user_id"):
        user = db.session.get(
            User,
            session["user_id"],
        )

        if user and user.is_admin:
            return redirect(url_for("students.list_students"))

        return redirect(url_for("students.profile"))

    if request.method == "POST":

        email = (
            request.form.get(
                "email",
                "",
            )
            .strip()
            .lower()
        )

        password = request.form.get(
            "password",
            "",
        )

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):

            flash(
                "Invalid email or password.",
                "danger",
            )

        else:

            session.clear()
            session["user_id"] = user.id

            flash(
                "Logged in successfully.",
                "success",
            )

            next_url = request.args.get("next")

            if next_url and next_url.startswith("/"):
                return redirect(next_url)

            if user.is_admin:
                return redirect(url_for("students.list_students"))

            return redirect(url_for("students.profile"))

    return render_template("auth/login.html")


@auth_bp.post("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out.",
        "info",
    )

    return redirect(url_for("auth.login"))
