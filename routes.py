from app import app
from flask import redirect, render_template, request, session
import messages
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
    result = db.session.execute("SELECT id, topic FROM cats")
    cats = result.fetchall()
    return render_template("main.html", count=len(cats), cats=cats, id=id)


@app.route("/threads/<int:id>")
def threads(id):
    result = db.session.execute(
        "SELECT topic FROM cats WHERE id=:id", {"id": id})
    topic = result.fetchone()[0]
    result = db.session.execute(
        "SELECT id, topic FROM threads where cat_id=:id", {"id": id})
    threads = result.fetchall()
    return render_template("threads.html", id=id, topic=topic, threads=threads)


@app.route("/new/<int:id>", methods=["GET"])
def newthread(id):
    return render_template("new.html", id=id)


@app.route("/new", methods=["POST"])
def new():
    topic = request.form["topic"]
    id = request.form["id"]
    if messages.post_thread(topic, id):
        return redirect("/main")
    else:
        return render_template("error.html", message="Thread creation failed")


@app.route("/messages/<int:id>", methods=["GET"])
def newmess(id):
    result = db.session.execute(
        "SELECT topic FROM threads WHERE id=:id", {"id": id})
    topic = result.fetchone()[0]
    result = db.session.execute(
        "SELECT id, content FROM messages where thread_id=:id", {"id": id})
    messages = result.fetchall()
    return render_template("messages.html", id=id, topic=topic, messages=messages)

@app.route("/messent", methods=["POST"])
def newmessent():
    content = request.form["message"]
    id = request.form["id"]
    if messages.post_message(content, id):
        return redirect("/main")
    else:
        return render_template("error.html", message="Message sending failed")