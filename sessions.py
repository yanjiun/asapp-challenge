import contextlib
import random
import string

# this module managers tokens & login sessions


def generate_token():
    token = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    return token


def login_user(conn, username, password):
    token = generate_token()
    exists, user_id = login_check(conn, username, password)
    if exists:
        update_user_token(conn, user_id, token)
    return user_id, token


def update_user_token(conn, user_id, token):
    with contextlib.closing(conn.cursor()) as cur:
        params = (user_id, token)
        cur.execute('''REPLACE INTO sessions(user_id, token) VALUES(?, ?) 
                     ''', params)
        conn.commit()
        # TODO: verify success

def authenticate(conn, user_id, token):
    # checks db to authenticate user tokens
    # return False if not authenticated
    with contextlib.closing(conn.cursor()) as cur:
        params = (user_id, )
        cur.execute('SELECT token from sessions where user_id=?', params)
        rows = cur.fetchall()
        if len(rows) > 0:
            return token == rows[0][0]
        else:
            return False


def login_check(conn, username, password):
    with contextlib.closing(conn.cursor()) as cur:
        params = (username, password)
        cur.execute('SELECT user_id from users where username=? and password=?', params)
        rows = cur.fetchall()
        if len(rows) <= 0:
            return (False, -1)
        else:
            return (True, rows[0][0])