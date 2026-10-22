
import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from database import get_db

registration_bp = Blueprint("registration", __name__)

@registration_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]
        department = request.form["department"].strip()

        if not all([name, email, password, department]):
            return "All fields are required", 400

        try:
            with get_db() as con:
                con.execute("""
                    INSERT INTO students
                    (name, email, password, department)
                    VALUES (?, ?, ?, ?)
                """, (
                    name,
                    email,
                    generate_password_hash(password),
                    department
                ))
        except sqlite3.IntegrityError:
            return "Email already registered", 409

        return redirect(url_for("login.login"))

    return render_template("register.html")
