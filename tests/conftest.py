import pytest

from app import create_app
from app.extensions import db


@pytest.fixture
def app(tmp_path):
    database_path = tmp_path / "test.db"

    app = create_app(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": False,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path}",
            "UPLOAD_FOLDER": str(tmp_path / "uploads"),
        }
    )

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
