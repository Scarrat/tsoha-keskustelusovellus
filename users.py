from app import app
from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session


def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)


def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            return True
        else:
            return False


def make_admin(user):
    try:
        sql = "UPDATE users SET admin = TRUE WHERE username = :user"
        db.session.execute(sql, {"user": user})
        db.session.commit()
        return True
    except:
        return False


def admin_status(user):
    sql = "SELECT admin FROM users WHERE username=:user"
    return db.session.execute(sql, {"user": user}).fetchone()[0]


def add_secret(id):
    try:
        sql = "INSERT INTO secret (user_id) VALUES (:id)"
        db.session.execute(sql, {"id": id})
        db.session.commit()
    except:
        return False
