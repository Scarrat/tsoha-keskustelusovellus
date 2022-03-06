from app import app
from db import db


def getThreads(id):
    result = db.session.execute(
        "SELECT topic FROM threads WHERE id=:id", {"id": id})
    return len(result)
