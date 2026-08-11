import os
import uuid
from ..forms import ProfilePictureForm
from ..forms import LoginForm, ProfilePictureForm
from flask_login import login_user, logout_user, login_required, current_user

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from flask_login import current_user, login_required, login_user, logout_user

from werkzeug.security import check_password_hash, generate_password_hash

from ..extensions import db
from ..models.user import User

auth_bp = Blueprint("auth", __name__)


# =========================
# REGISTER
# =========================


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("auth.profile"))

    if request.method == "POST":

        username = request.form.get("username", "").strip()

        password = request.form.get("password", "")

        if not username or not password:

            flash("Username and password are required.", "danger")

            return redirect(url_for("auth.register"))

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:

            flash("Username already exists.", "danger")

            return redirect(url_for("auth.register"))

        user = User(username=username, password=generate_password_hash(password))

        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


# =========================
# LOGIN
# =========================


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.profile"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.strip()).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)

            flash("Login successful!", "success")

            return redirect(url_for("auth.profile"))

        flash("Invalid username or password.", "danger")

    return render_template("login.html", form=form)


# =========================
# LOGOUT
# =========================


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))


# =========================
# PROFILE
# =========================


@auth_bp.route("/profile")
@login_required
def profile():
    form = ProfilePictureForm()
    return render_template("profile.html", form=form)


# =========================
# PROFILE PICTURE
# =========================


@auth_bp.route("/profile/upload", methods=["POST"])
@login_required
def upload_profile_picture():

    file = request.files.get("picture")

    if not file or not file.filename:

        flash("Please select an image.", "danger")

        return redirect(url_for("auth.profile"))

    extension = os.path.splitext(file.filename)[1].lower()

    allowed_extensions = {".jpg", ".jpeg", ".png", ".gif"}

    if extension not in allowed_extensions:

        flash("Only JPG, JPEG, PNG and GIF files are allowed.", "danger")

        return redirect(url_for("auth.profile"))

    filename = f"{uuid.uuid4()}{extension}"

    upload_folder = current_app.config["UPLOAD_FOLDER"]

    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, filename)

    file.save(filepath)

    current_user.profile_picture = filename

    db.session.commit()

    flash("Profile picture uploaded successfully!", "success")

    return redirect(url_for("auth.profile"))
