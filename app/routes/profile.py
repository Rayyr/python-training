from pathlib import Path
from flask import Blueprint, render_template, request, redirect, current_app, flash, url_for, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_PROFILE_EXTENSIONS"]

@profile_bp.route("/", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        file = request.files.get("profile_picture")
        if not file or not file.filename:
            flash("Choose an image first.", "error")
            return redirect(url_for("profile.profile"))

        if not allowed_file(file.filename):
            flash("Allowed formats: PNG, JPG, JPEG, GIF.", "error")
            return redirect(url_for("profile.profile"))

        upload_dir = Path(current_app.config["UPLOAD_FOLDER"])
        upload_dir.mkdir(parents=True, exist_ok=True)

        filename = secure_filename(f"user_{current_user.id}_{file.filename}")
        file.save(upload_dir / filename)
        current_user.profile_picture = filename

        from ..extensions import db
        db.session.commit()
        flash("Profile picture updated.", "success")
        return redirect(url_for("profile.profile"))

    return render_template("profile.html")

@profile_bp.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)
