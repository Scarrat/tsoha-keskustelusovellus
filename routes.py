from app import app
from flask import redirect, render_template, request, session
import users
from db import db


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username, password):
            return redirect("/main")
        else:
            return render_template("register.html", error="Registering failed")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/main")
        else:
            return render_template("error.html", message="Logging in failed")


@app.route("/main")
def main():
    result = db.session.execute("SELECT topic FROM cats")
    cats = result.fetchall()
    return render_template("main.html",count=len(cats), cats=cats)
