from flask import Blueprint,render_template,request,redirect,url_for
from ..models.student import Student
from ..extensions import db

student_bp=Blueprint("students",__name__,url_prefix="/students")

@student_bp.route("/")
def list_students():
    search=request.args.get("search","").strip()
    page=request.args.get("page",1,type=int)
    query=Student.query
    if search:
        query=query.filter(Student.name.ilike(f"%{search}%"))
    students=query.paginate(page=page,per_page=5,error_out=False)
    return render_template("students.html",students=students,search=search)

@student_bp.route("/add",methods=["POST"])
def add_student():
    student=Student(name=request.form["name"],email=request.form["email"])
    db.session.add(student)
    db.session.commit()
    return redirect(url_for("students.list_students"))
