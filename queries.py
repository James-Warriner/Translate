import sqlite3
from flask import g, session
from helpers import returnError
from werkzeug.security import check_password_hash

DATABASE = 'translate.db'


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
    try:
        cur = db.execute(query, args)
        db.commit()
    except sqlite3.IntegrityError as e:
        db.rollback()

        print("SQLite IntegrityError in query:")
        print("  SQL:   ", query)
        print("  ARGS:  ", args)
        print("  ERROR: ", e)
        if "user.email" in str(e):
            return returnError("That email is already registered.", 400)
        return returnError(f"Integrity error: {e}", 500)

    except sqlite3.Error as e:
        db.rollback()

        print("SQLite Error in query:")
        print("  SQL:   ", query)
        print("  ARGS:  ", args)
        print("  ERROR: ", e)
        return returnError(f"Database error: {e}", 500)

    if fetch:
        rows = [dict(row) for row in cur.fetchall()]
        return rows
    return None



def selectID(email):
    result = execute_query(
        "SELECT id FROM user WHERE email = ?",
        (email,),
        fetch=True
    )
    if not isinstance(result, list):
        return result
    if not result:
        return None
    return result[0]


def loginQuery(email, password):
    result = execute_query(
        "SELECT id, password_hash FROM user WHERE email = ?",
        (email,),
        fetch=True
    )

    if not isinstance(result, list):
        return result

    if not result:
        print(f"[loginQuery] no row for email={email!r}")
        return False

    row = result[0]
    user_id = row["id"]
    pw_hash = row["password_hash"]
    print(f"[loginQuery] user_id={user_id}, pw_hash={pw_hash!r}, password={password!r}")

    valid = check_password_hash(pw_hash, password)
    print(f"[loginQuery] check_password_hash returned {valid}")
    if valid:
        session["user_id"] = user_id
        print("[loginQuery] authentication successful")
        return True

    print("[loginQuery] authentication failed")
    return False


def getUser():
    if session.get("user_id") is not None:
        result = execute_query(
            "SELECT * FROM user WHERE id = ?",
            (session["user_id"],),
            fetch=True
        )
        if not isinstance(result, list):
            return result
        if result:
            user = result[0]
            print(user)
            return user
    return {"first_name": "", "last_name": "", "email": ""}

def speechTranslateUpload(og_audio,ogtxt,trnstxt,srclng,trgtlng):
    print("HERE")
    if session.get("user_id") is None:
        return False
    
    cmd = execute_query(
            "INSERT INTO translation (user_id,original_audio,original_text,type,translated_text,source_lang_id,target_lang_id) VALUES (?,?,?,?,?,?,?)",(session["user_id"],og_audio,ogtxt,'speech',trnstxt,srclng,trgtlng)
    )

    if cmd:
        print(cmd)
        return False
    else:
        return True
    

def textTranslateUpload(ogtxt,trnstxt,srclng,trgtlng):
    if session.get("user_id") is None:
        return False
    
    cmd = execute_query(
            "INSERT INTO translation (user_id,original_text,type,translated_text,source_lang_id,target_lang_id) VALUES (?,?,?,?,?,?)",(session["user_id"],ogtxt,'text',trnstxt,srclng,trgtlng)
    )

    if cmd:
        print(cmd)
        return False
    else:
        return True
    

def fetchRecents():
    if session.get("user_id") is None:
        return False
    
    res = execute_query("SELECT t.id,t.type, t.original_text, t.created_at AS date, src.code AS input_code, src.language AS input_language, tgt.code AS output_code, tgt.language AS output_language FROM translation AS t JOIN language_code AS src ON t.source_lang_id = src.id JOIN language_code AS tgt ON t.target_lang_id = tgt.id WHERE t.user_id = ? ORDER BY t.created_at DESC LIMIT 15", (session["user_id"],), fetch=True)

    

    if not res:

        return False
    
    return [dict(result)for result in res]
    