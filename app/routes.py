from flask import Blueprint, redirect, render_template, url_for

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")


@main.route("/login")
def login():
    return render_template("login.html")


@main.route("/register")
def register():
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
