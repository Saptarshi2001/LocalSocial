import sqlite3
def init_db():
    db=sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row
    #if db is not None:
    #    return
    with open('user.sql') as usr:
        db.executescript(usr.read())
    
    db.close()

def close_db(db):
    db.close()

init_db()
