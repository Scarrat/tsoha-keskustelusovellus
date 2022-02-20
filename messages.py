from db import db
import users


def post_thread(topic, id, user):
    db.session.execute("INSERT INTO threads (topic, created_at, cat_id, creator) values (:topic, NOW(), :id, :user)", {
                       "topic": topic, "id": id, "user": user})
    db.session.commit()
    return True


def post_message(content, id, user):
    db.session.execute("INSERT INTO messages (content, sent_at, thread_id, sender) values (:content, NOW(), :id, :user)", {
                       "content": content, "id": id, "user": user})
    db.session.commit()
    return True

def editt(id, content):
    db.session.execute("UPDATE threads SET topic=:content WHERE id=:id", {"content": content, "id": id})
    db.session.commit()
    return True

def editm(id, content):
    db.session.execute("UPDATE messages SET content=:content WHERE id=:id", {"content": content, "id": id})
    db.session.commit()
    return True

def deletet(id):
    db.session.execute("DELETE FROM threads WHERE id=:id", { "id": id})
    db.session.commit()
    return True

def deletem(id):
    db.session.execute("DELETE FROM messages WHERE id=:id", { "id": id})
    db.session.commit()
    return True