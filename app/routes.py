from flask import Blueprint, redirect, render_template, url_for, request, flash, session
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import User

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get form data
        username_or_email = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # Validate required fields
        if not username_or_email or not password:
            flash("Please enter your username/email and password.", "error")
            return render_template("login.html")

        # Find user by username or email
        user = User.query.filter(
            (User.username == username_or_email) |
            (User.email == username_or_email.lower())
        ).first()

        # Verify user and password
        if user is None or not user.check_password(password):
            flash("Invalid username/email or password.", "error")
            return render_template("login.html")

        # Store user ID in session
        session.clear()
        session["user_id"] = user.id

        flash("Login successful! Welcome back.", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("login.html")


@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get form data
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Validate required fields
        if not username or not email or not password:
            flash("Please fill in all fields.", "error")
            return render_template("register.html")

        # Check for existing username
        if User.query.filter_by(username=username).first():
            flash("This username is already taken.", "error")
            return render_template("register.html")

        # Check for existing email
        if User.query.filter_by(email=email).first():
            flash("This email address is already taken.", "error")
            return render_template("register.html")

        # Create new user
        new_user = User(
            username=username,
            email=email,
        )
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for("main.login"))

        except IntegrityError:
            db.session.rollback()
            flash("Username or email already exists.", "error")
            return render_template("register.html")
        
    return render_template("register.html")


@main.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@main.route("/transactions")
def transactions():
    return render_template("transactions.html")


@main.route("/logout")
def logout():
    return redirect(url_for("main.index"))
