from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import event
from sqlalchemy.engine import Engine

db=SQLAlchemy()
login_manager=LoginManager()
login_manager.login_view="auth.login"

@event.listens_for(Engine,"connect")
def enable_sqlite_foreign_keys(connection, record):
    cursor=connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
