import sqlite3
from flask import flash


def connect_db():
    db = sqlite3.connect('database.db')
    db.cursor().execute('CREATE TABLE IF NOT EXISTS posts '
                        '(id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, post TEXT)')
    db.cursor().execute('CREATE TABLE IF NOT EXISTS users '
                        '(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                        'email TEXT, password TEXT)')
    db.commit()
    return db

def add_user(email, password):
    db = connect_db()
    if db.cursor().execute('SELECT email FROM users where email=(?)',[email]).fetchone() is None:
        db.cursor().execute('INSERT INTO users (email, password) '
                            'VALUES (?, ?)', (email,password,))
        print("User added successfully")
        flash("Hey")
    else:
        print("user exists already")

    db.commit()

"""
def verify_user(email, password):
    db = connect_db()
    if db.cursor().execute('SELECT password FROM users where email=(?)',[email]).fetchone()[0]==password:
        print("User Exists")
        db.commit() 
        return 1
    else:
        print("nah")
        return None
"""
   
def get_id(email):
    db = connect_db()
    if db.cursor().execute('SELECT id FROM users where email=(?)',[email]).fetchone():
        print(db.cursor().execute('SELECT id FROM users where email=(?)',[email]).fetchone())
        return db.cursor().execute('SELECT id FROM users where email=(?)',[email]).fetchone()

def add_post(user,post):
    db = connect_db()
    db.cursor().execute('INSERT INTO posts (user,post) '
                        'VALUES (?,?)', (user,post,))
    db.commit()


def get_posts():
    db = connect_db()
    results = []
    get_all_query = 'SELECT * FROM posts'
    for (id,user,post,) in db.cursor().execute(get_all_query).fetchall():
            results.append((user,post))
    return results


