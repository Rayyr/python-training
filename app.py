from flask import Flask, render_template, request, redirect

app = Flask(__name__)

students = []  # in-memory storage

@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        student_id = request.form.get("id")
        email = request.form.get("email")

        if not name or not student_id or not email:
            return "Invalid input"

        students.append({
            "name": name,
            "id": student_id,
            "email": email
        })

        return redirect("/students")

    return render_template("form.html")


@app.route("/students")
def list_students():
    return render_template("students.html", students=students)


if __name__ == "__main__":
    app.run(debug=True)