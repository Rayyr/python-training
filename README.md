# 🎓 Student Portal v1 (Flask)

## 📌 Overview
This is a simple **Flask web application** built as part of Day 2 challenge.  
It allows users to:
- Register students
- View all students
- View individual student details

---

## 🚀 Features

- 🏠 Homepage with navigation
- 📝 Student registration form (POST)
- 📋 List of students (GET)
- 👤 Individual student detail page
- 🧪 Unit tests using pytest
- 🧱 Modular Flask structure (Blueprints)

---

## 🧱 Project Structure
project/
│
├── app/
│ ├── __init__.py
│ ├── routes.py
│ └── models.py
│
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── register.html
│ ├── students.html
│ └── student_detail.html
│
├── tests/
│ └── test_routes.py
│
├── run.py
├── requirements.txt
└── README.md
