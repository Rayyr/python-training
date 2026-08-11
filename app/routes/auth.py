from functools import wraps
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from app import db
from app.models.user import User
from app.models.student import Student

auth_bp = Blueprint("auth", __name__)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


@auth_bp.app_context_processor
def inject_current_user():
    user = db.session.get(User, session.get("user_id")) if session.get("user_id") else None
    return {"current_user": user}


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        if not name or not email or not password:
            flash("All fields are required.", "danger")
        elif len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
        elif password != confirm:
            flash("Passwords do not match.", "danger")
        elif User.query.filter_by(email=email).first():
            flash("An account with that email already exists.", "danger")
        else:
            user = User(name=name, email=email)
            user.set_password(password)

            # Create the matching Student record so a newly registered
            # account immediately appears in the Students list.
            student = Student(name=name, email=email)

            db.session.add(user)
            db.session.add(student)
            db.session.commit()
            session.clear()
            session["user_id"] = user.id
            flash("Account created successfully. Welcome!", "success")
            return redirect(url_for("students.list_students"))
    return render_template("auth/signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("Invalid email or password.", "danger")
        else:
            session.clear()
            session["user_id"] = user.id
            flash("Logged in successfully.", "success")
            next_url = request.args.get("next")
            return redirect(
                next_url
                if next_url and next_url.startswith("/")
                else url_for("students.list_students")
            )
    return render_template("auth/login.html")


@auth_bp.post("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
