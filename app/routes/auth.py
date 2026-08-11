import os
import uuid

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    current_app
)

from flask_login import login_required, current_user

from ..extensions import db
from ..forms import ProfilePictureForm


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/profile")
@login_required
def profile():
    form = ProfilePictureForm()

    return render_template(
        "profile.html",
        form=form
    )


@auth_bp.route("/profile/upload", methods=["POST"])
@login_required
def upload_profile_picture():
    form = ProfilePictureForm()

    if form.validate_on_submit():
        file = form.picture.data

        extension = os.path.splitext(
            file.filename
        )[1].lower()

        filename = f"{uuid.uuid4()}{extension}"

        upload_folder = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_folder, exist_ok=True)

        filepath = os.path.join(
            upload_folder,
            filename
        )

        file.save(filepath)

        # Remove the old file if one exists.
        old_picture = current_user.profile_picture

        if old_picture:
            old_path = os.path.join(
                upload_folder,
                old_picture
            )

            if os.path.exists(old_path):
                os.remove(old_path)

        current_user.profile_picture = filename

        db.session.commit()

        flash(
            "Profile picture uploaded successfully!",
            "success"
        )

        return redirect(
            url_for("auth.profile")
        )

    for field_errors in form.errors.values():
        for error in field_errors:
            flash(error, "danger")

    return redirect(
        url_for("auth.profile")
    )
