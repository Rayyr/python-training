# Week 9 Day 1 – Database Relations & CRUD Enhancements

## Features
- Many-to-many Student/Course relationship
- SQLAlchemy secondary enrollment table
- Cascade delete foreign keys
- Search and pagination
- Enrollment REST API
- Flask CLI seed command
- Relationship tests

## Run
pip install -r requirements.txt
python run.py

## Seed
flask seed

## Test
pytest

## Endpoints
POST /api/enrollment/
GET /api/enrollment/student/<student_id>
DELETE /api/enrollment/student/<student_id>/course/<course_id>

## Search
/students/?search=John&page=1
/courses/?search=Python&page=1

For the write enrollment endpoints, log in first because they use @login_required.
