from db import db
import users
def post_thread(topic):
    db.session.execute("INSERT INTO threads (topic, created_at) values (:topic, NOW())" ,{"topic":topic})
    db.session.commit()
    return True
