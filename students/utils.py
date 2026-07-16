# students/utils.py

import json
import csv
import os

FILE = "data/students.json"


def load_data():
    if not os.path.exists(FILE):
        return []

    if (os.path.getsize(FILE) == 0):
        return []

    with open(FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def export_csv(data, filename="students.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "student_id", "email", "grades"])
        writer.writeheader()
        writer.writerows(data)
