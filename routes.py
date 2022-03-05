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
        users.register(username, password)
        if username == "admin":
            users.make_admin(user)
        if users.login(username,password):
            session["username"] = username
            session["admin"] = users.admin_status(username)
            return redirect("/main")
        else:
            return render_template("error.html", error="Registering failed")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            session["username"] = username
            session["admin"] = users.admin_status(username)
            return redirect("/main")
        else:
            return render_template("error.html", message="Logging in failed")


@app.route("/logout")
def logout():
    del session["username"]
    if session["admin"]:
        del session["admin"]
    return redirect("/")


@app.route("/main")
def main():
    result = db.session.execute("SELECT id, topic, subcats, messagecount FROM cats ORDER BY id ASC")
    cats = result.fetchall()
    return render_template("main.html", count=len(cats), cats=cats)


@app.route("/threads/<int:id>")
def threads(id):
    result = db.session.execute(
        "SELECT topic FROM cats WHERE id=:id", {"id": id})
    topic = result.fetchone()[0]
    result = db.session.execute(
        "SELECT id, topic, creator, created_at FROM threads where cat_id=:id", {"id": id})
    threads = result.fetchall()
    return render_template("threads.html", count=len(threads), id=id, topic=topic, threads=threads)


@app.route("/new/<int:id>", methods=["GET"])
def newthread(id):
    return render_template("new.html", id=id)


@app.route("/new", methods=["POST"])
def new():
    topic = request.form["topic"]
    id = request.form["id"]
    user = request.form["user"]
    if messages.post_thread(topic, id, user):
        return redirect("/main")
    else:
        return render_template("error.html", message="Thread creation failed")

@app.route("/newsecret/", methods=["GET","POST"])
def newsecretthread():
    if request.method == "GET":
        return render_template("newsecret.html")
    if request.method == "POST":
        topic = request.form["topic"]
        user = request.form["user"]
        if messages.post_secretthread(topic,user):
            return redirect("/main")
        else:
            return render_template("error.html", message="Thread creation failed")

@app.route("/newcategory", methods=["GET", "POST"])
def newcategory():
    if request.method == "GET":
        return render_template("newcategory.html")
    if request.method == "POST":
        topic = request.form["topic"]
        if messages.post_category(topic):
            return redirect("/main")
        else:
            return render_template("error.html", message="Category creation failed")


@app.route("/messages/<int:id>", methods=["GET"])
def allmessages(id):
    result = db.session.execute(
        "SELECT topic FROM threads WHERE id=:id", {"id": id})
    topic = result.fetchone()[0]
    result = db.session.execute(
        "SELECT creator FROM threads WHERE id=:id", {"id": id})
    creator = result.fetchone()[0]
    result = db.session.execute(
        "SELECT messages.id, messages.sender, messages.sent_at, messages.content, users.id FROM messages, users WHERE messages.thread_id=:id AND messages.user_id = users.id", {"id": id})
    messages = result.fetchall()
    return render_template("messages.html", count=len(messages), id=id, messages=messages, topic=topic, creator=creator)


@app.route("/messent", methods=["POST"])
def newmessent():
    content = request.form["message"]
    id = request.form["id"]
    user = request.form["user"]
    type = request.form["type"]
    if messages.post_message(content, id, user,type):
        return redirect("/main")
    else:
        return render_template("error.html", message="Message sending failed")


@app.route("/editt", methods=["POST"])
def editt():
    content = request.form["content"]
    type = request.form["type"]
    if(type == "threadname"):
        thread_id = request.form["id"]
        if messages.editt(thread_id, content):
            return redirect("/main")
        else:
            return render_template("error.html", message="Editing failed")
    if(type == "message"):
        message_id = request.form["id"]
        if messages.editm(message_id, content):
            return redirect("/main")
        else:
            return render_template("error.html", message="Editing failed")
    if(type == "categoryname"):
        cat_id = request.form["id"]
        if messages.editc(cat_id, content):
            return redirect("/main")
        else:
            return render_template("error.html", message="Editing failed")



@app.route("/delete", methods=["POST"])
def delete():
    type = request.form["type"]
    if type=="thread":
        thread_id = request.form["id"]
        if messages.deletet(thread_id):
            return redirect("/main")
        else:
            return render_template("error.html", message="Deleting failed")
    if type=="message":
        message_id = request.form["id"]
        if messages.deletem(message_id):
            return redirect("/main")
        else:
            return render_template("error.html", message="Deleting failed")
    if type=="category":
        cat_id = request.form["id"]
        if messages.deletec(cat_id):
            return redirect("/main")
        else:
            return render_template("error.html", message="Deleting failed")
    if type=="secretmessage":
        message_id = request.form["id"]
        if messages.deletesm(message_id):
            return redirect("/main")
        else:
            return render_template("error.html", message="Deleting failed")

    if type=="secretthread":
        message_id = request.form["id"]
        if messages.deletest(message_id):
            return redirect("/main")
        else:
            return render_template("error.html", message="Deleting failed")

@app.route("/search", methods=["POST"])
def search():
    content = request.form["content"]
    result = db.session.execute(
        "SELECT * FROM messages WHERE content ILIKE :content", {"content": "%" + content + "%"})
    messages = result.fetchall()
    return render_template("search.html",messages=messages, list=list)

@app.route("/user/<int:id>")
def user(id):
    result = db.session.execute(
        "SELECT * FROM messages WHERE user_id =:id ", {"id":id})
    messages = result.fetchall()
    return render_template("user.html",messages= messages, id=id)

@app.route("/secretarea")
def secret():
    if session["admin"]:
        result = db.session.execute(
        "SELECT id, topic, creator, created_at FROM secretthreads")
        threads = result.fetchall()
        return render_template("secretarea.html", threads=threads)
    else:
        return render_template("error.html", message="No access")


@app.route("/secretmessages/<int:id>", methods=["GET"])
def secretmessages(id):
    result = db.session.execute(
        "SELECT topic FROM secretthreads WHERE id=:id", {"id": id})
    topic = result.fetchone()[0]
    result = db.session.execute(
        "SELECT creator FROM secretthreads WHERE id=:id", {"id": id})
    creator = result.fetchone()[0]
    result = db.session.execute(
        "SELECT secretmessages.id, secretmessages.sender, secretmessages.sent_at, secretmessages.content, users.id FROM secretmessages, users WHERE secretmessages.secretthread_id=:id AND secretmessages.user_id = users.id", {"id": id})
    messages = result.fetchall()
    return render_template("secretmessages.html", count=len(messages), id=id, messages=messages, topic=topic, creator=creator)
    

@app.route("/addsecret", methods=["POST"])
def addsecret():
    id = request.form["id"]
    user = db.session.execute("SELECT username FROM users WHERE id = :id", {"id":id}).fetchone()[0]
    if users.make_admin(user):
        return redirect("/main")
    else:
        return render_template("error.html", message="User already admin")

