from app.forms import LoginForm, ProfilePictureForm


def test_login_form_exists(app):
    with app.test_request_context():
        form = LoginForm()

        assert form is not None
        assert hasattr(form, "username")
        assert hasattr(form, "password")
        assert hasattr(form, "submit")


def test_login_form_requires_username_and_password(app):
    with app.test_request_context(method="POST", data={}):
        form = LoginForm()

        assert form.validate() is False
        assert form.username.errors
        assert form.password.errors


def test_profile_form_exists(app):
    with app.test_request_context():
        form = ProfilePictureForm()

        assert form is not None
        assert hasattr(form, "picture")
        assert hasattr(form, "submit")


def test_profile_form_requires_picture(app):
    with app.test_request_context(method="POST", data={}):
        form = ProfilePictureForm()

        assert form.validate() is False
        assert form.picture.errors
