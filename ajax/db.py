from os import name
import sqlite3


def connect_db():
    db = sqlite3.connect('database.db')
    db.cursor().execute('CREATE TABLE IF NOT EXISTS posts '
                        '(id INTEGER PRIMARY KEY, post TEXT)')
    db.cursor().execute('CREATE TABLE IF NOT EXISTS users '
                        '(user_id INTEGER PRIMARY KEY AUTOINCREMENT,email TEXT not null, password TEXT not null)')
    print("Opened database successfully")

    db.commit()
    #add_user('xyz@gmail.com', 'xyz123') #print("user added!")
    return db


def add_post(post):
    db = connect_db()
    db.cursor().execute('INSERT INTO posts (post) VALUES (?)', (post,))
    db.commit()


def get_posts():
    db = connect_db()
    results = []
    get_all_query = 'SELECT post FROM posts'
    for (post,) in db.cursor().execute(get_all_query).fetchall():
            results.append(post)
    return results

#DB function already added in 
"""
def add_user(email, password):
    db = connect_db()
    db.cursor().execute('INSERT INTO users (email, password) VALUES(?,?)', (email,password))
    db.commit()
    print("User Added")


def get_user():
    db = connect_db()
    results = []
    get_all_query = 'SELECT email, password FROM users'
    for (email, password,) in db.cursor().execute(get_all_query).fetchall():
            results.append([email,password])
    return results
    """