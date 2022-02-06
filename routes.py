from app import app
from flask import redirect, render_template, request, session
import messages, users
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
    result = db.session.execute("SELECT id, topic FROM cats")
    cats = result.fetchall()
    return render_template("main.html",count=len(cats), cats=cats, id=id)

@app.route("/threads/<int:id>")
def threads(id):
    result = db.session.execute("SELECT topic FROM cats WHERE id=:id",{"id":id})
    topic = result.fetchone()[0]
    result = db.session.execute("SELECT id, topic FROM threads where cat_id=:id", {"id":id})
    threads = result.fetchall()
    return render_template("threads.html", id=id, topic=topic, threads=threads)

@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "GET":
        return render_template("new.html")
    if request.method == "POST":
        topic = request.form["topic"]
        if messages.post_thread(topic):
            return redirect("/main")
        else:
            return render_template("error.html", message="Thread creation failed")

