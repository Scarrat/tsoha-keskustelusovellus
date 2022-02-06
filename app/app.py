from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
    return "Heipparallaa!"

@app.route("/main")
def main():
    result = db.session.execute("SELECT topic FROM categories")
    categories = result.fetchall()
    return render_template("main.html", count=len(categories), categories=categories) 

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    sql = "INSERT INTO threads (topic) VALUES (:content)"
    db.session.execute(sql, {"content":content})
    db.session.commit()
    return redirect("/General")

@app.route("/create", methods=["POST"])
def create():
    topic = request.form["topic"]
    sql = "INSERT INTO threads (topic, created_at) VALUES (:topic, NOW()) RETURNING id"
    result = db.session.execute(sql, {"topic":topic})
    thread_id = result.fetchone()[0]
    choices = request.form.getlist("choice")
    for choice in choices:
        if choice != "":
            sql = "INSERT INTO choices (poll_id, choice) VALUES (:poll_id, :choice)"
            db.session.execute(sql, {"poll_id":thread_id, "choice":choice})
    db.session.commit()
    return redirect("/")

@app.route("/General")
def general():
    sql = "SELECT id, topic, created_at FROM threads ORDER BY id DESC"
    result = db.session.execute(sql)
    threads = result.fetchall()
    return render_template("general.html", threads=threads)