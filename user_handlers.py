import contextlib

class UserAlreadyExists(Exception):
    pass

def get_next_user_id(conn):
    max_id = 0
    with contextlib.closing(conn.cursor()) as cur:
        cur.execute('SELECT max(user_id) from users')
        row = cur.fetchone()
        if row[0] is not None:
            max_id = row[0] + 1

    print("returning user id: %s" %max_id)
    return max_id

def create_user(conn, username, password):
    if not login_existence(conn, username):
        with contextlib.closing(conn.cursor()) as cur:
            user_id = get_next_user_id(conn)
            params = (user_id, username, password)
            cur.execute('''INSERT INTO users VALUES (?, ?, ?)''', params)
            conn.commit()
            return user_id
    else:
        print("login for username %s already exists" %username)
        raise UserAlreadyExists()


def login_existence(conn, username):
    with contextlib.closing(conn.cursor()) as cur:
        params = (username,)
        cur.execute('SELECT * from users where username=?', params)
        rows = cur.fetchall()
        if len(rows) <= 0:
            return False
        else:
            return True