# Week 9 Day 2 – Advanced Flask Features

## Features

- Flask-WTF forms
- CSRF protection
- File upload validation
- Student profile pictures
- User profile picture database field
- Flash messages
- Custom 404 page
- Custom 500 page
- Student/course search and pagination
- Enrollment API from Day 1

## Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Linux/macOS:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python run.py
```

Open:

```text
http://127.0.0.1:5000/students/
```

Profile page:

```text
http://127.0.0.1:5000/profile
```

The profile route requires a logged-in user.

## Uploads

Allowed:

- JPG
- JPEG
- PNG
- GIF

Maximum upload size is 5 MB.

Files are stored in:

```text
app/static/uploads/
```

## Tests

```bash
pytest
```

## Important

If you already have the Day 1 SQLite database, delete the old database before running this version if your database schema does not contain the new `profile_picture` column.

For a real production project, use Flask-Migrate/Alembic instead of deleting the database.
