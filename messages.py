from db import db
import users


def post_thread(topic, id, user):
    if topic:
        db.session.execute("INSERT INTO threads (topic, created_at, cat_id, creator) values (:topic, NOW(), :id, :user)", {
                        "topic": topic, "id": id, "user": user})
        db.session.execute("UPDATE cats SET subcats =subcats +1 where id=:id", {"id":id})
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
            user_id= db.session.execute("SELECT id FROM users where username =:user",{"user":user}).fetchone()[0]
            db.session.execute("INSERT INTO secretmessages (content, sent_at, secretthread_id, sender, user_id) values (:content, NOW(), :id, :user, :user_id)", {"content": content, "id": id, "user": user, "user_id":user_id})
            db.session.commit()
            return True
        user_id= db.session.execute("SELECT id FROM users where username =:user",{"user":user}).fetchone()[0]
        db.session.execute("INSERT INTO messages (content, sent_at, thread_id, sender, user_id) values (:content, NOW(), :id, :user, :user_id)", {
                       "content": content, "id": id, "user": user, "user_id":user_id})
        result = db.session.execute("SELECT cat_id FROM threads WHERE id=:id",{"id":id})
        theid = result.fetchone()[0]
        db.session.execute("UPDATE cats SET messagecount =messagecount +1 where id=:id", {"id":theid})
        db.session.commit()
        return True
    else:
        return False

def editt(id, content):
    db.session.execute("UPDATE threads SET topic=:content WHERE id=:id", {"content": content, "id": id})
    db.session.commit()
    return True

def editm(id, content):
    db.session.execute("UPDATE messages SET content=:content WHERE id=:id", {"content": content, "id": id})
    db.session.commit()
    return True

def editc(id, content):
    db.session.execute("UPDATE cats SET topic=:content WHERE id=:id", {"content": content, "id": id})
    db.session.commit()
    return True

def deletet(id):
    result = db.session.execute("SELECT cat_id FROM threads WHERE id=:id",{"id":id})
    id1 = result.fetchone()[0]
    db.session.execute("UPDATE cats SET subcats =subcats -1 where id=:id", {"id":id1})
    result = db.session.execute("select id from messages where thread_id=:id", {"id":id1})
    ids = result.fetchall()
    for x in ids:
        deletem(id)
    db.session.execute("DELETE FROM threads WHERE id=:id", { "id": id})
    db.session.commit()
    return True

def deletem(id):
    result = db.session.execute("SELECT thread_id FROM messages WHERE id=:id",{"id":id})
    id1 = result.fetchone()[0]
    result = db.session.execute("SELECT cat_id FROM threads WHERE id=:id",{"id":id1})
    id2 = result.fetchone()[0]
    db.session.execute("UPDATE cats SET messagecount =messagecount -1 where id=:id", {"id":id2})
    db.session.execute("DELETE FROM messages WHERE id=:id", { "id": id})
    db.session.commit()
    return True

def deletesm(id):
    db.session.execute("DELETE FROM secretmessages WHERE id=:id", { "id": id})
    db.session.commit()
    return True

def deletest(id):
    db.session.execute("DELETE FROM secretthreads WHERE id=:id", { "id": id})
    db.session.commit()
    return True

def deletec(id):
    db.session.execute("DELETE FROM cats WHERE id=:id" , { "id": id})
    db.session.commit()
    return True