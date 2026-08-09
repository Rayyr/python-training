from flask import Blueprint, render_template, request, redirect
from flask_login import login_user, logout_user, login_required
from ..models.user import User
from ..extensions import db, login_manager


auth_bp = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form["username"]
        ).first()

        if user and user.check_password(request.form["password"]):
            login_user(user)
            return redirect("/students/")

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")
