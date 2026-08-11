from flask import Blueprint,render_template,request,redirect,url_for
from ..models.course import Course
from ..extensions import db

course_bp=Blueprint("courses",__name__,url_prefix="/courses")

@course_bp.route("/")
def list_courses():
    search=request.args.get("search","").strip()
    page=request.args.get("page",1,type=int)
    query=Course.query
    if search:
        query=query.filter(Course.title.ilike(f"%{search}%"))
    courses=query.paginate(page=page,per_page=5,error_out=False)
    return render_template("courses.html",courses=courses,search=search)

@course_bp.route("/add",methods=["POST"])
def add_course():
    course=Course(title=request.form["title"])
    db.session.add(course)
    db.session.commit()
    return redirect(url_for("courses.list_courses"))
