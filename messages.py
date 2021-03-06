from queue import Empty
from sqlite3 import IntegrityError
from xmlrpc.client import boolean
from db import db
import users


def post_thread(topic, id, user):
    if topic:
        db.session.execute("INSERT INTO threads (topic, created_at, cat_id, creator) values (:topic, NOW(), :id, :user)", {
            "topic": topic, "id": id, "user": user})
        db.session.commit()
        return True
    else:
        return False


def post_secretthread(topic, user):
    if topic:
        db.session.execute("INSERT INTO secretthreads (topic, created_at, creator) values (:topic, NOW(), :user)", {
            "topic": topic, "id": id, "user": user})
        db.session.commit()
        return True
    else:
        return False


def post_category(topic):
    if topic:
        db.session.execute("INSERT INTO cats (topic) values (:topic)", {
            "topic": topic})
        db.session.commit()
        return True
    else:
        return False


def post_message(content, id, user, type):
    if content:
        if type == "secretmessage":
            user_id = db.session.execute("SELECT id FROM users where username =:user", {
                                         "user": user}).fetchone()[0]
            db.session.execute("INSERT INTO secretmessages (content, sent_at, secretthread_id, sender, user_id) values (:content, NOW(), :id, :user, :user_id)", {
                               "content": content, "id": id, "user": user, "user_id": user_id})
            db.session.commit()
            return True
        user_id = db.session.execute("SELECT id FROM users where username =:user", {
                                     "user": user}).fetchone()[0]
        db.session.execute("INSERT INTO messages (content, sent_at, thread_id, sender, user_id) values (:content, NOW(), :id, :user, :user_id)", {
            "content": content, "id": id, "user": user, "user_id": user_id})
        db.session.execute(
            "UPDATE threads SET last_sent =( NOW()) where id =:id", {"id": id})
        catid = db.session.execute("SELECT cat_id FROM threads where id=:id", {
                                   "id": id}).fetchone()[0]
        db.session.execute(
            "UPDATE cats SET last_sent=NOW() where id =:id", {"id": catid})
        db.session.commit()
        return True
    else:
        return False


def editt(id, content):
    db.session.execute("UPDATE threads SET topic=:content WHERE id=:id", {
                       "content": content, "id": id})
    db.session.commit()
    return True


def editm(id, content):
    db.session.execute("UPDATE messages SET content=:content WHERE id=:id", {
                       "content": content, "id": id})
    db.session.commit()
    return True


def editsm(id, content):
    db.session.execute("UPDATE secretmessages SET content=:content WHERE id=:id", {
                       "content": content, "id": id})
    db.session.commit()
    return True

def editst(id, content):
    db.session.execute("UPDATE secretthreads SET topic=:content WHERE id=:id", {
                       "content": content, "id": id})
    db.session.commit()
    return True

def editc(id, content):
    db.session.execute("UPDATE cats SET topic=:content WHERE id=:id", {
                       "content": content, "id": id})
    db.session.commit()
    return True


def deletet(id):
    result = db.session.execute(
        "select id from messages where thread_id=:id", {"id": id})
    ids = result.fetchall()
    for x in ids:
        deletem(x[0])
    db.session.execute("DELETE FROM threads WHERE id=:id", {"id": id})
    db.session.commit()
    return True


def deletem(id):
    db.session.execute("DELETE FROM messages WHERE id=:id", {"id": id})
    db.session.commit()
    return True


def deletesm(id):
    db.session.execute("DELETE FROM secretmessages WHERE id=:id", {"id": id})
    db.session.commit()
    return True


def deletest(id):
    db.session.execute("DELETE FROM secretthreads WHERE id=:id", {"id": id})
    db.session.commit()
    return True


def deletec(id):
    result = db.session.execute(
        "SELECT id FROM threads WHERE cat_id =:id", {"id": id}).fetchall()
    for x in result:
        deletet(x[0])
    db.session.execute("DELETE FROM cats WHERE id=:id", {"id": id})
    db.session.commit()
    return True
