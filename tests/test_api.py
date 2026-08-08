import pytest
from app import create_app
from app.extensions import db

@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_create_user(client):
    res = client.post('/api/users/', json={'username': 'test', 'password': '123'})
    assert res.status_code == 201

def test_get_users(client):
    client.post('/api/users/', json={'username': 'test', 'password': '123'})
    res = client.get('/api/users/')
    assert res.status_code == 200

def test_create_student(client):
    res = client.post('/api/students/', json={'name': 'nada'})
    assert res.status_code == 201

def test_get_students(client):
    res = client.get('/api/students/')
    assert res.status_code == 200

def test_create_course(client):
    res = client.post('/api/courses/', json={'title': 'Math'})
    assert res.status_code == 201
