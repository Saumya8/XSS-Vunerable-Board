import sqlite3


def connect_db():
    db = sqlite3.connect('database.db')
    db.cursor().execute('CREATE TABLE IF NOT EXISTS posts '
                        '(id INTEGER PRIMARY KEY, '
                        'post TEXT)')
    db.commit()
    return db


def add_post(post):
    db = connect_db()
    db.cursor().execute('INSERT INTO posts (post) '
                        'VALUES (?)', (post,))
    db.commit()


def get_posts():
    db = connect_db()
    results = []
    get_all_query = 'SELECT post FROM posts'
    for (post,) in db.cursor().execute(get_all_query).fetchall():
            results.append(post)
    return results
