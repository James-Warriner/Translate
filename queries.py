import sqlite3
from flask import g

DATABASE = 'translate.db'  # or set this via app config if you prefer

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def execute_query(query, args=(), fetch=False):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()

    if fetch:
        return [dict(row) for row in cur.fetchall()]
    else:
        return None

