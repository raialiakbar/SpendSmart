from functools import wraps

from flask import (
    Blueprint,
    flash, 
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import User

auth = Blueprint("auth", __name__)


def login_required(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "error")
            return redirect(url_for("auth.login"))

        return route_function(*args, **kwargs)
    return decorated_function


@auth.route("/login", methods=["GET", "POST"])
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


@auth.route("/register", methods=["GET", "POST"])
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
            return redirect(url_for("auth.login"))

        except IntegrityError:
            db.session.rollback()
            flash("Username or email already exists.", "error")
            return render_template("register.html")
        
    return render_template("register.html")


@auth.route("/logout", methods=["POST"])
def logout():
    session.clear()

    flash("You have been logged out successfully.", "success")
    return redirect(url_for("main.index"))