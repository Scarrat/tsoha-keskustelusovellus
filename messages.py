from db import db
import users
def post_thread(topic, id):
    db.session.execute("INSERT INTO threads (topic, created_at, cat_id) values (:topic, NOW(), :id)" ,{"topic":topic, "id":id})
    db.session.commit()
    return True

def post_message(content, id):
    db.session.execute("INSERT INTO messages (content, sent_at, thread_id) values (:content, NOW(), :id)" ,{"content":content, "id":id})
    db.session.commit()
    return True
