import sqlite3
from flask import flash


def connect_db():
    db = sqlite3.connect('database.db')
    db.cursor().execute('CREATE TABLE IF NOT EXISTS posts '
                        '(id INTEGER PRIMARY KEY, '
                        'post TEXT)')
    db.cursor().execute('CREATE TABLE IF NOT EXISTS users '
                        '(id INTEGER PRIMARY KEY, '
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

def get_users():
    db = connect_db()
    results = []
    get_all_query = 'SELECT * FROM users'
    for (id,email,password,) in db.cursor().execute(get_all_query).fetchall():
            results.append((email,password))
    return results
   


