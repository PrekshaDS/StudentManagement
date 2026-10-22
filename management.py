from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session
)
from database import get_db

management_bp = Blueprint("management", __name__)


@management_bp.route("/students")
def students():
    if "student_id" not in session:
        return redirect(url_for("login.login"))

    with get_db() as con:
        student = con.execute(
            "SELECT id, name, email, department "
            "FROM students WHERE id = ?",
            (session["student_id"],)
        ).fetchone()

    if student is None:
        session.clear()
        return redirect(url_for("login.login"))

    return render_template("students.html", student=student)


@management_bp.route("/students/update", methods=["POST"])
def update_student():
    if "student_id" not in session:
        return redirect(url_for("login.login"))

    name = request.form["name"].strip()
    department = request.form["department"].strip()

    if not name or not department:
        return "Name and department are required", 400

    with get_db() as con:
        con.execute(
            "UPDATE students SET name = ?, department = ? "
            "WHERE id = ?",
            (name, department, session["student_id"])
        )

    return redirect(url_for("management.students"))


@management_bp.route("/students/delete", methods=["POST"])
def delete_student():
    if "student_id" not in session:
        return redirect(url_for("login.login"))

    with get_db() as con:
        con.execute(
            "DELETE FROM students WHERE id = ?",
            (session["student_id"],)
        )

    session.clear()
    return redirect(url_for("home"))