from app.forms import ProfilePictureForm


def test_profile_form_exists(app):
    with app.test_request_context():
        form = ProfilePictureForm()
        assert form is not None


def test_profile_form_has_picture_field(app):
    with app.test_request_context():
        form = ProfilePictureForm()
        assert hasattr(form, "picture")
